.. _User guide Cirq:

Cirq on IQM User Guide
======================

This guide serves as an introduction to the main features of Cirq on IQM, the Cirq adapter for IQM Client.
You are encouraged to run the demonstrated code snippets and check the output yourself.


Installation
------------

.. note::

    If you have previously installed the (now deprecated) ``cirq-iqm`` package in your Python environment,
    you should first uninstall it with ``$ pip uninstall cirq-iqm``. In this case, you should also include
    the ``--force-reinstall`` option in the ``iqm-client`` installation command.

The recommended way is to install the optional ``cirq`` feature of the ``iqm-client`` distribution package directly
from the Python Package Index (PyPI):

.. code-block:: bash

   $ pip install iqm-client[cirq]


After installation, Cirq on IQM can be imported in your Python code as follows:

.. code-block:: python

   from iqm import cirq_iqm


IQM's quantum devices
---------------------

Cirq on IQM provides descriptions of IQM's quantum architectures using the :class:`.IQMDevice` class, which is a
subclass of :class:`cirq.devices.Device` and implements general functionality relevant to all IQM devices. The native
gates and connectivity of the architecture are available in the :class:`.IQMDeviceMetadata` object returned by the
:attr:`.IQMDevice.metadata` property. It is possible to use the IQMDevice class directly, but
certain devices with predefined metadata are also available as subclasses of IQMDevice. As an example, let
us import the class :class:`.Adonis`, which describes IQM's five-qubit architecture, and view some of its
properties contained in its ``metadata`` property:

.. code-block:: python

    from iqm.cirq_iqm import Adonis

    adonis = Adonis()

    print(adonis.metadata.qubit_set)
    print(adonis.metadata.gateset)
    print(adonis.metadata.nx_graph)


IQM devices use :class:`cirq.NamedQubit` to represent their qubits. The names of the qubits consist of a prefix
followed by a numeric index, so we have qubit names like ``QB1``, ``QB2``, etc. Note that we use 1-based
indexing. You can get the list of the qubits in a particular device by accessing the :attr:`qubits` attribute of a
corresponding :class:`.IQMDevice` instance:

.. code-block:: python

    print(adonis.qubits)


Constructing circuits
---------------------

There are two main ways of constructing :class:`cirq.Circuit` instances for IQM devices:

1. Create a ``Circuit`` instance using arbitrary qubit names and types.
2. Create a ``Circuit`` from an OpenQASM 2.0 program. The qubit names are determined by the OpenQASM ``qreg`` names,
   appended with zero-based indices.

Below we give an example of each method.


Method 1
^^^^^^^^

Construct a circuit and use arbitrary qubits:

.. code-block:: python

    import cirq

    q1, q2 = cirq.NamedQubit('Alice'), cirq.NamedQubit('Bob')
    circuit = cirq.Circuit()
    circuit.append(cirq.X(q1))
    circuit.append(cirq.H(q2))
    circuit.append(cirq.CNOT(q1, q2))
    circuit.append(cirq.measure(q1, q2, key='m'))
    print(circuit)

This will result in the circuit
::

   Alice: ───X───@───M('m')───
                 │   │
   Bob: ─────H───X───M────────


Method 2
^^^^^^^^

You can read an OpenQASM 2.0 program from a file (or a string), e.g.

::

   OPENQASM 2.0;
   include "qelib1.inc";

   qreg q[2];
   creg m[2];

   x q[0];
   h q[1];
   cx q[0], q[1];
   measure q -> m;

and convert it into a :class:`cirq.Circuit` object using :func:`.circuit_from_qasm`.

.. code-block:: python

    from iqm import cirq_iqm

    with open('circuit.qasm', 'r') as f:
        qasm_circuit = cirq_iqm.circuit_from_qasm(f.read())
    print(qasm_circuit)

::

   q_0: ───X───@───M('m_0')───
               │
   q_1: ───H───X───M('m_1')───

:func:`.circuit_from_qasm` uses the OpenQASM 2.0 parser in :mod:`cirq.contrib.qasm_import`.

After a circuit has been constructed, it can be decomposed and routed against a particular :class:`.IQMDevice`.


Decomposition
-------------

The method :meth:`.IQMDevice.decompose_circuit` accepts a :class:`cirq.Circuit` object as an argument and
returns the decomposed circuit containing only native operations for the corresponding device:

.. code-block:: python

    decomposed_circuit = adonis.decompose_circuit(circuit)
    print(decomposed_circuit)

::

    Alice: ───X────────────────────@───────────M('m')───
                                   │           │
    Bob: ─────Y^0.5───X───Y^-0.5───@───Y^0.5───M────────

The Hadamard and CNOT gates are not native to Adonis, so they were decomposed to X, Y and CZ gates which are.


.. _routing:

Routing
-------

Routing means transforming a circuit such that it acts on the device qubits, and respects the
device connectivity.
The method :meth:`.IQMDevice.route_circuit` accepts a :class:`cirq.Circuit` object as an argument,
and returns the circuit routed against the device, acting on the device qubits instead of the
arbitrary qubits we had originally.

.. code-block:: python

    routed_circuit_1, initial_mapping, final_mapping = adonis.route_circuit(decomposed_circuit)
    print(routed_circuit_1)

::

    QB3: ───X────────────────────@───────────M('m')───
                                 │           │
    QB4: ───Y^0.5───X───Y^-0.5───@───Y^0.5───M────────

Along with the routed circuit :meth:`.route_circuit` returns the ``initial_mapping`` and ``final_mapping``.
The ``initial_mapping`` is either the mapping from circuit to device qubits as provided by an
:class:`cirq.AbstractInitialMapper` or a mapping that is initialized from the device graph.
The ``final_mapping`` is the mapping from physical qubits before inserting SWAP gates to the physical
qubits after the routing is complete

As mentioned above, you may also provide the initial mapping from the *logical* qubits in the circuit to the
*physical* qubits on the device yourself, by using the keyword argument ``initial_mapper``.
It serves as the starting point of the routing:

.. code-block:: python

    initial_mapper = cirq.HardCodedInitialMapper({q1: adonis.qubits[2], q2: adonis.qubits[0]})
    routed_circuit_2, _, _ = adonis.route_circuit(
        decomposed_circuit,
        initial_mapper=initial_mapper,
    )
    print(routed_circuit_2)

::

    QB1: ───Y^0.5───X───Y^-0.5───@───Y^0.5───────M────────
                                 │               │
    QB3: ───X────────────────────@───────────────M('m')───

Under the hood, :meth:`.route_circuit` leverages the routing provided by :class:`cirq.RouteCQC`.
It works on single- and two-qubit gates, and measurement operations of arbitrary size.
If you have gates involving more than two qubits you need to decompose them before routing.
Since routing may add some SWAP gates to the circuit, you will need to decompose the circuit
again after the routing, unless SWAP is a native gate for the target device.

To ensure that the transpiler is restricted to a specific subset of qubits, you can provide a list
of qubits in the ``qubit_subset`` argument such that ancillary qubits will not be added during
routing. This is particularly useful when running Quantum Volume benchmarks.

IQM Star architecture
^^^^^^^^^^^^^^^^^^^^^

Devices that have the IQM Star architecture (e.g. IQM Deneb) contain
computational resonators in addition to qubits, and use qubit-resonator gates instead of two-qubit
gates. These include the MOVE gate which moves qubit states to and from the resonators.
There are two main supported workflows for the Star architecture:

1. Construct your circuit as you would for a regular qubits-only device, decompose (and optimize)
   it to native gates, and then route it using :meth:`.IQMDevice.route_circuit`.
   This will attempt to route all the (fictional) two-qubit gates in the circuit through the
   resonator(s) using the native gates, adding MOVE gates as necessary.
   Under the hood, this uses the :func:`~iqm.iqm_client.transpile.transpile_insert_moves` function of the
   :mod:`~iqm.iqm_client` library.

2. Construct your circuit directly using the device qubits, resonators, and qubit-resonator gates,
   routing it manually.

Advanced users can use :func:`.transpile_insert_moves_into_circuit` to transpile circuits that
have some MOVE gates in them in addition to fictional qubit-qubit gates.

Optimization
------------

Yet another important topic is circuit optimization. In addition to the optimizers available in Cirq you can also
benefit from Cirq on IQM's :mod:`.optimizers` module which contains some optimization tools geared towards IQM devices.
The function :func:`.optimizers.simplify_circuit` is a convenience method encapsulating a particular sequence of
optimizations. Let us try it out on our decomposed and routed circuit above:

.. code-block:: python

    from iqm.cirq_iqm.optimizers import simplify_circuit

    simplified_circuit = simplify_circuit(routed_circuit_1)
    print(simplified_circuit)


::

    QB3: ───PhX(1)───@───────────────────M('m')───
                     │                   │
    QB4: ────────────@───PhX(-0.5)^0.5───M────────


.. note::

    The funtion :func:`.simplify_circuit` is not associated with any IQM device, so its result may contain non-native
    gates for a particular device. In the example above we don't have them, however it is generally a good idea to run
    decomposition once again after the simplification.

Classical control
-----------------

Some IQM quantum computers support classically-controlled gates, that is, gates that are executed
conditionally depending on the result of a measurement preceding them in the quantum circuit. This
support currently has several limitations:

* Only the ``PhasedXPowGate``, ``XPowGate`` and ``YPowGate`` gates can be classically controlled.
* The gates can only be conditioned on the measurement result of a single qubit, and the only control available is to
  apply the gate if the result is 1, and apply an identity gate if the result is 0.
* The availability of the controlled gates depends on the instrumentation of the quantum computer.

The classical control can be applied on an operation using :meth:`~cirq.Operation.with_classical_controls`:

.. code-block:: python

    import cirq
    q1, q2 = cirq.NamedQubit('Alice'), cirq.NamedQubit('Bob')
    circuit = cirq.Circuit(
        cirq.X(q1),
        cirq.measure(q1, key='A'),
        cirq.X(q2).with_classical_controls('A'),
        cirq.measure(q1, q2, key='final'),
    )
    print(circuit)

::

    Alice: ───X───M───────M('final')───
                  ║       │
    Bob: ─────────╫───X───M────────────
                  ║   ║
    A: ═══════════@═══^════════════════

After an ``X`` gate is applied on ``Alice``, the qubit is measured and the result is stored
in the key ``A``. If the result is 1 (which it should always be in this case),
another ``X`` gate is subsequently applied on ``Bob``. If it is 0, an identity gate of corresponding
duration is applied instead.

The ``final`` measurement in the above circuit should always return `11`, even though ``Alice`` and ``Bob`` are never
actually entangled.

.. note::

   Because classically controlled gates can currently only take feedback from one classical bit you must condition
   them on a measurement key that only measures a single qubit.

Resetting qubits
----------------

The :class:`cirq.R` operation can be used to reset qubits to the :math:`|0\rangle` state.
It is currently implemented as a (projective) measurement followed by a classically controlled X
gate conditioned on the result, and is only available if the quantum computer supports
classically controlled gates.

.. code-block:: python

    import cirq
    q1 = cirq.NamedQubit('q1')
    circuit = cirq.Circuit(cirq.X(q1), cirq.R(q1), cirq.measure(q1))
    circuit

::

    q1: ───X───R───M───

In the above example, the X gate prepares the qubit ``q1`` in a :math:`|1\rangle` state,
and the reset then collapses it back into the :math:`|0\rangle` state.
Executing the circuit should result in (mostly) zeros being measured.


Running on a real quantum computer
----------------------------------

.. note::

   You can access IQM quantum computers via `IQM Resonance <https://www.meetiqm.com/products/iqm-resonance>`_
   or use one of the IQM quantum computers deployed at HPC centers and research institutions around the globe.

Cirq contains various simulators which you can use to simulate the circuits constructed above.
In this subsection we demonstrate how to run them on an IQM quantum computer.

Cirq on IQM provides :class:`.IQMSampler`, a subclass of :class:`cirq.work.Sampler`, which is used
to execute quantum circuits and decompose/route them for the architecture of the quantum computer.
Once you have access to an IQM server you can create an :class:`.IQMSampler` instance and use its
:meth:`~.IQMSampler.run` method to send a circuit for execution and retrieve the results:

.. code-block:: python

   from iqm.cirq_iqm.iqm_sampler import IQMSampler

   # circuit = ...

   sampler = IQMSampler(iqm_server_url)
   decomposed_circuit = sampler.device.decompose_circuit(circuit)
   routed_circuit, _, _ = sampler.device.route_circuit(decomposed_circuit)
   result = sampler.run(routed_circuit, repetitions=10)
   print(result.measurements['m'])


Note that the code snippet above assumes that you have set the variable ``iqm_server_url`` to the URL
of the IQM server. Additionally, you can pass IQM backend specific options to the :class:`.IQMSampler` class.
The below table summarises the currently available options:


.. list-table::
   :widths: 25 20 25 100
   :header-rows: 1

   * - Name
     - Type
     - Example value
     - Description
   * - :attr:`calibration_set_id`
     - :class:`uuid.UUID`
     - "f7d9642e-b0ca-4f2d-af2a-30195bd7a76d"
     - Indicates the calibration set to use. Defaults to ``None``, which means the IQM server will use the
       current default calibration set automatically.
   * - :attr:`compiler_options`
     - :class:`~iqm.iqm_client.models.CircuitCompilationOptions`
     - see below
     - Contains various options that affect the compilation of the quantum circuit into an
       instruction schedule.

The :class:`~iqm.iqm_client.models.CircuitCompilationOptions` class contains the following attributes (in addition to some
advanced options described in the API documentation):

.. list-table::
   :widths: 25 20 25 100
   :header-rows: 1

   * - Name
     - Type
     - Example value
     - Description
   * - :attr:`max_circuit_duration_over_t2`
     - :class:`float` | :class:`None`
     - 1.0
     - Set server-side circuit disqualification threshold. If any circuit in a job is estimated to take longer than the
       shortest T2 time of any qubit used in the circuit multiplied by this value, the server will reject the job.
       Setting this value to ``0.0`` will disable circuit duration check.
       The default value ``None`` means the server default value will be used.
   * - :attr:`heralding_mode`
     - :class:`~iqm.iqm_client.models.HeraldingMode`
     - "zeros"
     - Heralding mode to use during execution. The default value is "none", "zeros" enables
       all-zeros heralding where the circuit qubits are measured before the circuit begins, and the
       server post-selects and returns only those shots where the heralding measurement yields zeros
       for all the qubits.

For example if you would like to use a particular calibration set, you can provide it as follows:

.. code-block:: python

   sampler = IQMSampler(iqm_server_url, calibration_set_id="f7d9642e-b0ca-4f2d-af2a-30195bd7a76d")


The sampler will by default use an :class:`.IQMDevice` created based on architecture data obtained
from the server, which is then available in the :attr:`.IQMSampler.device` property. The architecture
data depends on the calibration set used by the sampler, so one should usually use different sampler
instances for different calibration sets. Alternatively, the device can be specified directly with
the :attr:`device` argument, but this is not recommended when running on a real quantum computer.

When executing a circuit that uses something other than the device qubits, you need to route it first,
as explained in the :ref:`routing` section above.


Authentication
^^^^^^^^^^^^^^

IQM Resonance
"""""""""""""

If you are using IQM Resonance, you have two options to authenticate:

1. Set the :envvar:`IQM_TOKEN` environment variable with the API token obtained from the Resonance dashboard.
2. Pass the ``token`` parameter to :class:`.IQMSampler`. This will be forwarded to
   :class:`~iqm.iqm_client.iqm_client.IQMClient`.

On-premises devices
"""""""""""""""""""

If the IQM server you are connecting to requires authentication, you may use
:ref:`IQM Client CLI <User guide CLI>` to retrieve and automatically refresh access tokens,
then set the :envvar:`IQM_TOKENS_FILE` environment variable, as instructed, to point to the tokens file.
See IQM Client CLI's `documentation <https://docs.meetiqm.com/iqm-client/user_guide_cli.html>`__ for details.

Alternatively, you may authenticate yourself using the :envvar:`IQM_AUTH_SERVER`,
:envvar:`IQM_AUTH_USERNAME` and :envvar:`IQM_AUTH_PASSWORD` environment variables, or pass them as
arguments to :class:`.IQMSampler`, but this approach is less secure and
considered deprecated.


Batch execution
^^^^^^^^^^^^^^^

Multiple circuits can be submitted to the IQM quantum computer at once using the
:meth:`~.IQMSampler.run_iqm_batch` method of :class:`.IQMSampler`.  This is often faster than
executing the circuits individually. Circuits submitted in a batch are still executed sequentially.

.. code-block:: python

   circuit_list = []

   circuit_list.append(routed_circuit_1)
   circuit_list.append(routed_circuit_2)

   results = sampler.run_iqm_batch(circuit_list, repetitions=10)

   for result in results:
        print(result.histogram(key="m"))


Inspecting the final circuits before submitting them for execution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to inspect the final circuits that would be submitted for execution before actually submitting them,
which can be useful for debugging purposes. This can be done using :meth:`.IQMSampler.create_run_request`, which returns
a :class:`~iqm.iqm_client.models.RunRequest` containing the circuits and other data. The method accepts the same
parameters as :meth:`.IQMSampler.run` and :meth:`.IQMSampler.run_iqm_batch`, and creates the run request in the same
way as those functions.

.. code-block:: python

    # inspect the run_request without submitting it for execution
    run_request = sampler.create_run_request(routed_circuit_1, repetitions=10)
    print(run_request)

    # the following calls submit exactly the same run request for execution on the server
    sampler.run(routed_circuit_1, repetitions=10)
    sampler._client.submit_run_request(run_request)


It is also possible to print a run request when it is actually submitted by setting the environment variable
:envvar:`IQM_CLIENT_DEBUG=1`.


More examples
-------------

More examples are available in the
`Cirq on IQM examples directory <https://github.com/iqm-finland/sdk/tree/main/iqm_client/src/iqm/cirq_iqm/examples>`_
of the IQM Client repository.


