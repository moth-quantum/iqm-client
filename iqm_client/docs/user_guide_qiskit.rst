.. _User guide Qiskit:

Qiskit on IQM User Guide
=========================

This guide illustrates the main features of Qiskit on IQM, the Qiskit adapter for IQM Client.
You are encouraged to run the demonstrated code snippets and check the output yourself.

.. note::

   IQM provides access to its quantum computers via IQM Resonance – IQM's quantum cloud service.
   Please head over `to our website <https://www.meetiqm.com/products/iqm-resonance/>`_ to learn more.


Hello, world!
-------------

Here's a quick and easy way to run a small computation on an IQM quantum computer to check that
things are set up correctly, either
through the IQM cloud service Resonance, or using an on-premises quantum computer.

IQM Resonance
~~~~~~~~~~~~~

1. Login to `IQM Resonance <https://resonance.meetiqm.com>`_ with your credentials.
2. Upon your first visit to IQM Resonance, you can generate your unique, non-recoverable API token
   directly from the Dashboard page by selecting ``Generate token``. It's important to copy the token
   immediately from the window, as you won't be able to do so once the window is closed. If you lose
   your token, you have the option to regenerate it at any time. However, be aware that regenerating
   your API token will invalidate any previously generated token.
3. Download one of the demo notebooks from `IQM Academy <https://www.iqmacademy.com/tutorials/>`_ or the
   `resonance_example.py example file <https://raw.githubusercontent.com/iqm-finland/sdk/main/iqm-client/src/iqm/qiskit_iqm/examples/resonance_example.py>`_
   (Save Page As...)
4. Install Qiskit on IQM as instructed below.
5. Add your API token to the example (either as the parameter ``token`` to the :class:`.IQMProvider`
   constructor, or by setting the environment variable :envvar:`IQM_TOKEN`)
6. Run the Jupyter notebook (or run ``python resonance_example.py`` if you decided to go for the Python script).
7. If you're connecting to a real quantum computer, the output should show almost half of the
   measurements resulting in '00000' and almost half in '11111' - if this is the case, things are
   set up correctly!

You can find a video guide on how to set things up `here <https://www.iqmacademy.com/tutorials/resonance/>`_.
More ready-to-run examples can also be found at `IQM Academy <https://www.iqmacademy.com/tutorials/>`_.


On-premises device
~~~~~~~~~~~~~~~~~~

1. Download the `bell_measure.py example file <https://raw.githubusercontent.com/iqm-finland/sdk/main/iqm-client/src/iqm/qiskit_iqm/examples/bell_measure.py>`_ (Save Page As...).
2. Install Qiskit on IQM as instructed below.
3. Install IQM Client CLI and log in as instructed in the
   `documentation <https://docs.meetiqm.com/iqm-client/user_guide_cli.html#installing-iqm-client-cli>`__
4. Set the environment variable as instructed by IQM Client CLI after logging in.
5. Run ``$ python bell_measure.py --cortex_server_url https://demo.qc.iqm.fi/cocos`` - replace the example URL with the correct one.
6. If you're connecting to a real quantum computer, the output should show almost half of the
   measurements resulting in '00' and almost half in '11' - if this is the case, things are set up
   correctly!


Installation
------------

.. note::

    If you have previously installed the (now deprecated) ``qiskit-iqm`` package in your Python environment,
    you should first uninstall it with ``$ pip uninstall qiskit-iqm``. In this case, you should also include
    the ``--force-reinstall`` option in the ``iqm-client`` installation command.

The recommended way is to install the optional ``qiskit`` feature of the ``iqm-client`` distribution package directly
from the Python Package Index (PyPI):

.. code-block:: bash

   $ pip install iqm-client[qiskit]


After installation, Qiskit on IQM can be imported in your Python code as follows:

.. code-block:: python

   from iqm import qiskit_iqm


Authentication
--------------

IQM Resonance
~~~~~~~~~~~~~

If you are using IQM Resonance, you have two options to authenticate:

1. Set the :envvar:`IQM_TOKEN` environment variable to the API token obtained from the Resonance dashboard.
2. Pass the ``token`` parameter to :class:`.IQMProvider`. This will be forwarded to
   :class:`~iqm.iqm_client.iqm_client.IQMClient`. For an example, see the `resonance_example.py file
   <https://raw.githubusercontent.com/iqm-finland/sdk/main/iqm-client/src/iqm/qiskit_iqm/examples/resonance_example.py>`_

On-premises devices
~~~~~~~~~~~~~~~~~~~

If the IQM server you are connecting to requires authentication, you may use
:ref:`IQM Client CLI <User guide CLI>` to retrieve and automatically refresh access tokens,
then set the :envvar:`IQM_TOKENS_FILE` environment variable, as instructed, to point to the tokens file.
See IQM Client CLI's `documentation <https://docs.meetiqm.com/iqm-client/user_guide_cli.html>`__ for details.

You may also authenticate yourself using the :envvar:`IQM_AUTH_SERVER`,
:envvar:`IQM_AUTH_USERNAME` and :envvar:`IQM_AUTH_PASSWORD` environment variables, or pass them as
arguments to :class:`.IQMProvider`, however this approach is less secure and considered deprecated.


Running quantum circuits on an IQM quantum computer
---------------------------------------------------

In this section we demonstrate the practicalities of using Qiskit on IQM to execute
quantum circuits on an IQM quantum computer.

.. _GHZ_circuit:

Executing a circuit
~~~~~~~~~~~~~~~~~~~

Let's consider the following quantum circuit which prepares and measures a GHZ state:

.. code-block:: python

    from qiskit import QuantumCircuit

    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(0, 2)
    circuit.measure_all()

    print(circuit.draw(output='text'))

::

            ┌───┐           ░ ┌─┐
       q_0: ┤ H ├──■────■───░─┤M├──────
            └───┘┌─┴─┐  │   ░ └╥┘┌─┐
       q_1: ─────┤ X ├──┼───░──╫─┤M├───
                 └───┘┌─┴─┐ ░  ║ └╥┘┌─┐
       q_2: ──────────┤ X ├─░──╫──╫─┤M├
                      └───┘ ░  ║  ║ └╥┘
    meas: 3/═══════════════════╩══╩══╩═
                               0  1  2


To run this circuit on an IQM quantum computer you need to initialize an :class:`.IQMProvider`
instance with the IQM server URL, use it to retrieve an :class:`.IQMBackend` instance representing
the quantum computer, and use Qiskit's :func:`~qiskit.compiler.transpile` function
followed by :meth:`.IQMBackend.run` as usual.  ``shots`` denotes the number of times the quantum
circuit(s) are sampled:

.. code-block:: python

    from qiskit import transpile
    from iqm.qiskit_iqm import IQMProvider

    iqm_server_url = "https://demo.qc.iqm.fi/cocos/"  # Replace this with the correct URL
    provider = IQMProvider(iqm_server_url)
    backend = provider.get_backend()

    transpiled_circuit = transpile(circuit, backend=backend)
    job = backend.run(transpiled_circuit, shots=1000)


.. note::

   As of ``qiskit >= 1.0``, Qiskit no longer supports :func:`execute`. Instead you should
   first transpile the circuit and then run it, as shown in the code above.
   See the :ref:`transpilation` section to learn how to transpile circuits in various ways.

.. note::

   If you want to inspect the circuits that are sent to the device, use the ``circuit_callback``
   keyword argument of :meth:`.IQMBackend.run`. See also
   `Inspecting circuits before submitting them for execution`_ for inspecting the actual run request sent for
   execution.

You can optionally provide IQMBackend specific options as additional keyword arguments to
:meth:`.IQMBackend.run`, documented at :meth:`.IQMBackend.create_run_request`.
For example, you can enable heralding measurements using ``circuit_compilation_options`` as follows:

.. code-block:: python

    from iqm.iqm_client import CircuitCompilationOptions

    job = backend.run(transpiled_circuit, shots=1000, circuit_compilation_options=CircuitCompilationOptions(heralding_mode=HeraldingMode.ZEROS))


Calibration
~~~~~~~~~~~

The calibration data for an IQM quantum computer is stored in a *calibration set*. An :class:`.IQMBackend` instance
always corresponds to a specific calibration set, so that its transpilation target uses only those QPU components
(qubits and computational resonators) and gates which are available in that calibration set. The server default
calibration set will be used by default, but you can also use a different calibration set by specifying the
``calibration_set_id`` parameter to :meth:`.IQMProvider.get_backend` or :class:`.IQMBackend`. If the server default
calibration set has changed after you have created the backend, the backend will still use the original default calibration
set when submitting circuits for execution. When this happens you will get a warning.
You will need to create a new backend if you want to use the new default calibration set instead.

Inspecting the results
~~~~~~~~~~~~~~~~~~~~~~

The results of a job that was executed on the IQM quantum computer, represented as a
:class:`~qiskit.result.Result` instance, can be inspected using the usual Qiskit methods:

.. code-block:: python

    result = job.result()
    print(result.get_counts())
    print(result.get_memory())

The result comes with some metadata, such as the :class:`~iqm.iqm_client.models.RunRequest` that
produced it in ``result.request``. The request contains e.g. the qubit mapping and the ID of the
calibration set that were used in the execution:

.. code-block:: python

    print(result.request.qubit_mapping)
    print(result.request.calibration_set_id)

::

    [
      SingleQubitMapping(logical_name='0', physical_name='QB1'),
      SingleQubitMapping(logical_name='1', physical_name='QB2'),
      SingleQubitMapping(logical_name='2', physical_name='QB3')
    ]
    1320eae6-f4e2-424d-b299-ef82d556d2c3

Another piece of useful metadata are the timestamps of the various steps of processing the job. The
timestamps are stored in the dict ``result.timestamps``. The job processing has three steps,

* ``compile`` where the circuits are converted to instruction schedules,
* ``submit`` where the instruction schedules are submitted for execution, and
* ``execution`` where the instruction schedules are executed and the measurement results are returned.

The dict contains a timestamp for the start and end of each step.
For example, the timestamp of starting the circuit compilation is stored with key ``compile_start``.
In the same way the other steps have their own timestamps with keys consisting of the step name and a ``_start`` or
``_end`` suffix. In addition to processing step timestamps, there are also timestamps for the job itself,
``job_start`` for when the job request was received by the server and ``job_end`` for when the job processing
was finished.

If the processing of the job is terminated before it is complete, for example due to an error, the timestamps of
processing steps that were not taken are not present in the dict.

For example:

.. code-block:: python

    print(result.timestamps['job_start'])
    print(result.timestamps['compile_start'])
    print(result.timestamps['execution_end'])


Backend properties
~~~~~~~~~~~~~~~~~~

The :class:`.IQMBackend` instance we created above provides all the standard backend functionality that one expects from a
backend in Qiskit. For this example, I am connected to an IQMBackend that features a 5-qubit chip with star-like
connectivity:

::

          QB1
           |
    QB2 - QB3 - QB4
           |
          QB5

Let's examine its basis gates and the coupling map through the ``backend`` instance

.. code-block:: python

    print(f'Native operations of the backend: {backend.operation_names}')
    print(f'Coupling map of the backend: {backend.coupling_map}')

::

    Native operations of the backend: ['id', 'r', 'cz', 'measure']
    Coupling map of the backend: [[0, 2], [2, 0], [1, 2], [2, 1], [2, 3], [3, 2], [2, 4], [4, 2]]

Note that for IQMBackends the identity gate ``id`` is not actually a gate that is executed on the device and is simply omitted.
At IQM we identify qubits by their names, e.g. 'QB1', 'QB2', etc. as demonstrated above. In Qiskit, qubits are
identified by their indices in the quantum register, as you can see from the printed coupling map above. Most of the
time you do not need to deal with IQM-style qubit names when using Qiskit, however when you need, the methods
:meth:`.IQMBackendBase.qubit_name_to_index` and :meth:`.IQMBackendBase.index_to_qubit_name` can become handy.


Classically controlled gates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some IQM quantum computers support classically controlled gates, that is, gates that are executed
conditionally depending on the result of a measurement preceding them in the quantum circuit. This
support currently has several limitations:

* Only the ``x``, ``y``, ``rx``, ``ry`` and ``r`` gates can be classically controlled.
* The gates can only be conditioned on one classical bit, and the only control available is to
  apply the gate if the bit is 1, and apply an identity gate if the bit is 0.
* The availability of the controlled gates depends on the instrumentation of the quantum computer.

The classical control can be applied on a circuit instruction using :meth:`~qiskit.circuit.Instruction.c_if`:

.. code-block:: python

    from qiskit import QuantumCircuit

    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(1, 'c')
    circuit = QuantumCircuit(qr, cr)

    circuit.h(0)
    circuit.measure(0, cr[0])
    circuit.x(1).c_if(cr, 1)
    circuit.measure_all()

    print(circuit.draw(output='text'))

::

            ┌───┐┌─┐        ░ ┌─┐
       q_0: ┤ H ├┤M├────────░─┤M├───
            └───┘└╥┘ ┌───┐  ░ └╥┘┌─┐
       q_1: ──────╫──┤ X ├──░──╫─┤M├
                  ║  └─╥─┘  ░  ║ └╥┘
                  ║ ┌──╨──┐    ║  ║
       c: 1/══════╩═╡ 0x1 ╞════╬══╬═
                  0 └─────┘    ║  ║
    meas: 2/═══════════════════╩══╩═
                               0  1


The first measurement operation stores its result in the 1-bit classical register ``c``. If the
result is 1, the ``X`` gate will be applied. If it is zero, an identity gate of corresponding
duration is applied instead.

Executing the above circuit should result in the counts being approximately 50/50 split
between the '00 0' and '11 1' bins of the histogram (even though the state itself is never entangled).

.. note::

   Because the gates can only take feedback from one classical bit you must place the measurement result
   in a 1-bit classical register, ``c`` in the above example.


Resetting qubits
~~~~~~~~~~~~~~~~

The :class:`qiskit.circuit.Reset` operation can be used to reset qubits to the :math:`|0\rangle` state.
It is currently implemented as a (projective) measurement followed by a classically controlled X gate conditioned
on the result, and is only available if the quantum computer supports classically controlled gates.

.. code-block:: python

    from qiskit import QuantumCircuit

    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.reset(0)
    circuit.measure(0, 0)

    print(circuit.draw(output='text'))

::

         ┌───┐     ┌─┐
      q: ┤ H ├─|0>─┤M├
         └───┘     └╥┘
    c: 1/═══════════╩═
                    0

In the above example, the Hadamard gate prepares a uniform superposition of the :math:`|0\rangle` and
:math:`|1\rangle` states, and the reset then collapses it back into the :math:`|0\rangle` state.
Executing the circuit should result in (mostly) zeros being measured.


Inspecting circuits before submitting them for execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to inspect the final circuits that would be submitted for execution before actually submitting them,
which can be useful for debugging purposes. This can be done using :meth:`.IQMBackend.create_run_request`, which returns
a :class:`~iqm.iqm_client.models.RunRequest` containing the circuits and other data. The method accepts the same
parameters as :meth:`.IQMBackend.run`.

.. code-block:: python

    # inspect the run_request without submitting it for execution
    run_request = backend.create_run_request(transpiled_circuit, shots=10)
    print(run_request)

    # the following two calls submit exactly the same run request for execution on the server
    backend.run(transpiled_circuit, shots=10)
    backend.client.submit_run_request(run_request)

It is also possible to print a run request when it is actually submitted by setting the environment variable
``IQM_CLIENT_DEBUG=1``.


.. _transpilation:

Transpilation
-------------

In this section we study how the circuit gets transpiled in more detail.


Basic transpilation
~~~~~~~~~~~~~~~~~~~

You can use the default Qiskit transpiler on IQM quantum computers with both
the Crystal and the Star architectures.
Starting from the :ref:`GHZ circuit <GHZ_circuit>` we created above:

.. code-block:: python

    from qiskit.compiler import transpile

    transpiled_circuit = transpile(circuit, backend=backend, layout_method='sabre', optimization_level=3)
    print(transpiled_circuit.draw(output='text', idle_wires=False))

::

    global phase: 3π/2
              ┌─────────────┐                  ┌─────────────┐ ░       ┌─┐
    q_2 -> 5  ┤ R(π/2,3π/2) ├──────────■───────┤ R(π/2,5π/2) ├─░───────┤M├
              ├─────────────┤          │       └─────────────┘ ░ ┌─┐   └╥┘
    q_0 -> 10 ┤ R(π/2,3π/2) ├─■────────■───────────────────────░─┤M├────╫─
              ├─────────────┤ │ ┌─────────────┐                ░ └╥┘┌─┐ ║
    q_1 -> 15 ┤ R(π/2,3π/2) ├─■─┤ R(π/2,5π/2) ├────────────────░──╫─┤M├─╫─
              └─────────────┘   └─────────────┘                ░  ║ └╥┘ ║
      meas: 3/════════════════════════════════════════════════════╩══╩══╩═
                                                                0  1  2


Under the hood the Qiskit transpiler uses the :class:`.IQMDefaultSchedulingPlugin` plugin that
automatically adapts the transpiled circuit to the IQMBackend. In particular,

* if ``optimization_level > 0``, the plugin will use the :class:`.IQMOptimizeSingleQubitGates`
  pass to optimize single-qubit gates, and
* for devices that have the IQM Star architecture, the plugin will use the
  :class:`.IQMNaiveResonatorMoving` pass to automatically insert :class:`.MoveGate` instructions
  as needed.

Alternatively, you can use the :func:`transpile_to_IQM` function for more precise control over the
transpilation process as documented below.

It is also possible to use one of our other pre-defined transpiler plugins as an argument to
:func:`~qiskit.compiler.transpile`, for example
``transpile(circuit, backend=backend, scheduling_method="only_move_routing_keep")``.
Additionally, you can use any of our transpiler passes
to define your own :class:`qiskit.transpiler.PassManager` if you want to assemble custom
transpilation procedures manually.


Computational resonators
~~~~~~~~~~~~~~~~~~~~~~~~

The IQM Star architecture includes computational resonators as additional QPU components,
and uses qubit-resonator gates instead of two-qubit gates. These include
:class:`.MoveGate` which moves qubit states to and from the resonators.

The standard Qiskit transpiler does not know how to compile qubit-resonator gates.
This is why IQMBackend provides the Qiskit transpiler a *simplified* transpilation target in which
the resonators and MOVE gates have been abstracted away, and replaced with fictional two-qubit gates
that directly connect qubits that can be made to interact via a resonator. It then
uses :class:`.IQMDefaultSchedulingPlugin` to re-introduce resonators and add
:class:`MOVE gates <.MoveGate>` between qubits and resonators as necessary at the scheduling stage.

IQMDefaultSchedulingPlugin is executed automatically when you use the Qiskit transpiler.
Starting from the :ref:`GHZ circuit <GHZ_circuit>` we created above:

.. code-block:: python

    from qiskit.compiler import transpile
    from iqm.qiskit_iqm import IQMProvider

    resonator_backend = IQMProvider("https://cocos.resonance.meetiqm.com/deneb").get_backend()
    transpiled_circuit = transpile(circuit, resonator_backend)

    print(transpiled_circuit.draw(output='text', idle_wires=False))

::

                   ┌─────────────┐┌───────┐                  ┌───────┐                ░ ┌─┐
          q_0 -> 0 ┤ R(π/2,3π/2) ├┤0      ├──────────────────┤0      ├────────────────░─┤M├──────
                   ├─────────────┤│       │   ┌─────────────┐│       │                ░ └╥┘┌─┐
          q_1 -> 1 ┤ R(π/2,3π/2) ├┤       ├─■─┤ R(π/2,5π/2) ├┤       ├────────────────░──╫─┤M├───
                   ├─────────────┤│  Move │ │ └─────────────┘│  Move │┌─────────────┐ ░  ║ └╥┘┌─┐
          q_2 -> 2 ┤ R(π/2,3π/2) ├┤       ├─┼────────■───────┤       ├┤ R(π/2,5π/2) ├─░──╫──╫─┤M├
                   └─────────────┘│       │ │        │       │       │└─────────────┘ ░  ║  ║ └╥┘
        resonators ───────────────┤1      ├─■────────■───────┤1      ├───────────────────╫──╫──╫─
                                  └───────┘                  └───────┘                   ║  ║  ║
           meas: 3/══════════════════════════════════════════════════════════════════════╩══╩══╩═
                                                                                     0  1  2


Custom transpilation
~~~~~~~~~~~~~~~~~~~~

As an alternative to the native Qiskit transpiler integration, you can use the
:func:`.transpile_to_IQM` function.  It is meant for users who want at least one of the following:

* more fine grained control over the transpilation process without having to figure out which IQM
  transpiler plugin to use,
* transpile Star architecture circuits that already contain qubit-resonator gates, or
* force the transpiler to use a strict subset of qubits on the device.

For example, if you want to transpile the circuit with ``optimization_level=0`` but also apply the
single qubit gate optimization pass, you can do one of the following, equivalent things:

.. code-block:: python

    transpile_to_IQM(circuit, backend=backend, optimization_level=0, perform_move_routing=False, optimize_single_qubits=True)

.. code-block:: python

    transpile(circuit, backend=backend, optimization_level=0, scheduling_method='only_rz_optimization')

Similarly, if you want to transpile a native Star architecture circuit that already contains
:class:`.MoveGate` instances (that act on a qubit and a computational resonator), you can do the following:

.. code-block:: python

    from iqm.iqm_client.transpile import ExistingMoveHandlingOptions
    from iqm.qiskit_iqm import IQMCircuit, transpile_to_IQM

    move_circuit = IQMCircuit(3)
    move_circuit.h(0)
    move_circuit.move(0, 1)
    move_circuit.h(2)
    move_circuit.cz(2, 1)
    move_circuit.h(2)
    move_circuit.move(0, 1)

    # Using transpile() does not work here, as the circuit already contains a MoveGate
    transpiled_circuit = transpile_to_IQM(move_circuit, backend=resonator_backend, existing_moves_handling=ExistingMoveHandlingOptions.KEEP)
    print(transpiled_circuit.draw(output='text', idle_wires=False))

::

             ┌─────────────┐┌───────┐   ┌───────┐
    q_0 -> 0 ┤ R(π/2,3π/2) ├┤0      ├───┤0      ├───────────────
             ├─────────────┤│       │   │       │┌─────────────┐
    q_2 -> 1 ┤ R(π/2,3π/2) ├┤  Move ├─■─┤  Move ├┤ R(π/2,5π/2) ├
             └─────────────┘│       │ │ │       │└─────────────┘
    q_1 -> 6 ───────────────┤1      ├─■─┤1      ├───────────────
                            └───────┘   └───────┘

And if you want force the compiler to use a strict subset of qubits on the device, you can do the following:

.. code-block:: python

    qubits = [4, 3, 8]
    # or qubits = ['QB5', 'QB4', 'QB9']
    transpiled_circuit = transpile_to_IQM(circuit, backend=backend, restrict_to_qubits=qubits)
    print(transpiled_circuit.draw(output='text', idle_wires=False))

::

    global phase: 3π/2
             ┌─────────────┐   ┌─────────────┐                ░    ┌─┐
    q_1 -> 0 ┤ R(π/2,3π/2) ├─■─┤ R(π/2,5π/2) ├────────────────░────┤M├───
             ├─────────────┤ │ └─────────────┘                ░ ┌─┐└╥┘
    q_0 -> 1 ┤ R(π/2,3π/2) ├─■────────■───────────────────────░─┤M├─╫────
             ├─────────────┤          │       ┌─────────────┐ ░ └╥┘ ║ ┌─┐
    q_2 -> 2 ┤ R(π/2,3π/2) ├──────────■───────┤ R(π/2,5π/2) ├─░──╫──╫─┤M├
             └─────────────┘                  └─────────────┘ ░  ║  ║ └╥┘
     meas: 3/════════════════════════════════════════════════════╩══╩══╩═
                                                                 0  1  2

Note that if you do this, you do need to provide the :meth:`.IQMBackend.run` method a qubit
mapping that matches the restriction:

.. code-block:: python

    qubit_mapping = {i: backend.index_to_qubit_name(q) for i, q in enumerate(qubits)}
    job = backend.run(transpiled_circuit, qubit_mapping=qubit_mapping)


Using custom IQM transpiler plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the native integration of the custom IQM transpiler passes with the Qiskit transpiler, we
have implemented several scheduling plugins for the Qiskit transpiler. These plugins can be used as
the ``scheduling_method`` string argument for :func:`~qiskit.compiler.transpile`.
The mapping between these strings and the classes that implement the plugins is defined in the
:file:`pyproject.toml` file of this package.
The documentation of these plugins in found in the respective plugin classes.

If you are unsure which plugin to use, you can use :func:`.transpile_to_IQM` with the appropriate
arguments. This function determines which plugin to use based on the backend and the provided
arguments.  Note that the Qiskit transpiler automatically uses the
:class:`.IQMDefaultSchedulingPlugin` when the backend is an IQMBackend.


Batch execution of circuits
---------------------------

It is possible to submit multiple circuits to be executed, as a batch. In many cases this is more
time efficient than running the circuits one by one. Batch execution has some restrictions: all the
circuits must be executed for the same number of shots. For starters,
let's construct two circuits preparing and measuring different Bell states:

.. code-block:: python

    qc_1 = QuantumCircuit(2)
    qc_1.h(0)
    qc_1.cx(0, 1)
    qc_1.measure_all()

    qc_2 = QuantumCircuit(2)
    qc_2.h(0)
    qc_2.x(1)
    qc_2.cx(0, 1)
    qc_2.measure_all()

Now, we can run them together in a batch:

.. code-block:: python

    transpiled_qcs = transpile([qc_1, qc_2], backend=backend, initial_layout=[0, 2])
    job = backend.run(transpiled_qcs, shots=1000)
    print(job.result().get_counts())

The batch execution functionality can be used to run a parameterized circuit for various concrete values of parameters:

.. code-block:: python

    import numpy as np
    from qiskit.circuit import Parameter

    circuit = QuantumCircuit(2)
    theta = Parameter('theta')
    theta_range = np.linspace(0, np.pi / 2, 3)

    circuit.h(0)
    circuit.cx(0, 1)
    circuit.rz(theta, [0, 1])
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure_all()


    transpiled_circuit = transpile(circuit, backend=backend, layout_method='sabre', optimization_level=3)
    circuits = [transpiled_circuit.assign_parameters({theta: n}) for n in theta_range]
    job = backend.run(circuits, shots=1000)
    print(job.result().get_counts())

Note that it is important to transpile the parameterized circuit before binding the values to ensure a consistent qubit
measurements across circuits in the batch.


Multiplexed measurements
------------------------

When multiple measurement instructions are present in a circuit, the measurements may be multiplexed, meaning the
measurement pulses would be simultaneously executed on the quantum hardware, if possible. Multiplexing requires the
measurement instructions to form a convex subgraph, i.e. not have other instructions between them acting on the same
qubits.

You don't have to do anything special to enable multiplexing, it is automatically attempted by the
circuit-to-pulse compiler on the server side. However, you can ensure multiplexing (whenever
possible on the hardware level) by putting a ``barrier`` instruction before and after a group of
measurements.  This prevents the transpiler from inserting any other instructions between the
measurements.  There is no concept of multiplexed or simultaneous measurements in Qiskit, so the
circuit diagram will not indicate any multiplexing::

             ░ ┌─┐       ░
       q_0: ─░─┤M├───────░─
             ░ └╥┘┌─┐    ░
       q_1: ─░──╫─┤M├────░─
             ░  ║ └╥┘┌─┐ ░
       q_2: ─░──╫──╫─┤M├─░─
             ░  ║  ║ └╥┘ ░
    meas: 3/════╩══╩══╩═══
                0  1  2


Simulation
----------

In this section we show how to simulate the execution of quantum circuits on IQM quantum computers.

.. note::

   Since the simulation happens locally, you do not need access to an actual quantum computer.


Noisy simulation of quantum circuit execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The execution of circuits can be simulated locally, with a noise model to mimic the real hardware as
much as possible.  To this end, Qiskit on IQM provides the class :class:`.IQMFakeBackend` that can
be instantiated with properties of a certain QPU, e.g. using functions such as
:func:`.IQMFakeAdonis`, :func:`.IQMFakeApollo` and :func:`.IQMFakeAphrodite`
that represent specific IQM quantum architectures with pre-defined, representative noise models.

.. code-block:: python

    from qiskit import transpile, QuantumCircuit
    from iqm.qiskit_iqm import IQMFakeAdonis

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    backend = IQMFakeAdonis()
    transpiled_circuit = transpile(circuit, backend=backend)
    job = backend.run(transpiled_circuit, shots=1000)
    print(job.result().get_counts())


Above, we use an :func:`.IQMFakeAdonis` instance to run a noisy simulation of ``circuit`` on a simulated 5-qubit Adonis chip.
The noise model includes relaxation (:math:`T_1`) and dephasing (:math:`T_2`), gate infidelities and readout errors.
If you want to customize the noise model instead of using the default one provided by :func:`.IQMFakeAdonis`, you can create
a copy of the IQMFakeBackend instance with an updated error profile:

.. code-block:: python

    error_profile = backend.error_profile
    error_profile.t1s['QB2'] = 30000.0  # Change T1 time of QB2 as example
    custom_fake_backend = backend.copy_with_error_profile(error_profile)

Running a quantum circuit on a facade backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Circuits can be executed against a mock environment: an IQM server that has no real quantum computer hardware.
Results from such executions are random bits. This may be useful when developing and testing software integrations.

Qiskit on IQM contains :class:`.IQMFacadeBackend`, which allows to combine the mock remote execution with a local
noisy quantum circuit simulation. This way you can both validate your integration as well as get an idea of the expected circuit execution results.

To run a circuit this way, use the ``"facade_adonis"`` backend retrieved from the provider. Note that the provider must be
initialized with the URL of a quantum computer with the equivalent architecture (i.e. names of qubits, their
connectivity, and the native gateset should match the 5-qubit Adonis architecture).

.. code-block:: python

    from qiskit import transpile, QuantumCircuit
    from iqm.qiskit_iqm import IQMProvider

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    iqm_server_url = "https://demo.qc.iqm.fi/cocos/"  # Replace this with the correct URL
    provider = IQMProvider(iqm_server_url)
    backend = provider.get_backend('facade_adonis')
    transpiled_circuit = transpile(circuit, backend=backend)
    job = backend.run(transpiled_circuit, shots=1000)
    print(job.result().get_counts())

.. note::

   When a classical register is added to the circuit, Qiskit fills it with classical bits of value 0 by default. If the
   register is not used later, and the circuit is submitted to the IQM server, the results will not contain those
   0-filled bits. To make sure the facade backend returns results in the same format as a real IQM server,
   :meth:`.IQMFacadeBackend.run` checks for the presence of unused classical registers, and fails with an error if there
   are any.
