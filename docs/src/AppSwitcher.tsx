import React, { useState } from 'react';
import LogoSwitcher from './img/switcher.svg';
import LogoDocs from './img/docs.svg';
import LogoAcademy from './img/academy.svg';
import LogoResonance from './img/resonance.svg';
import LogoSupport from './img/support.svg';

const AppSwitcher: React.FC = () => {
    const [switcherOpen, setSwitcherOpen] = useState(false);

    const handleSwitcher = () => {
        setSwitcherOpen(!switcherOpen);
    };

    return (
        <div className="flex items-center pt-2 w-56 p-0">
            <button
                className="cursor-pointer p-0 border-none bg-transparent"
                onClick={handleSwitcher}
            >
                <img
                    className="title-image cursor-pointer"
                    alt="IQM Docs Application Switcher"
                    src={LogoSwitcher}
                    height={42}
                    width={222}
                    style={{ height: "42px", width: "222px" }}
                />
            </button>
            {switcherOpen && (
                <div className="absolute mt-[14em] ml-[0.5em] bg-white w-[208px] rounded-lg p-1 pt-1 z-50 border border-gray-300">
                    <div>
                        <a href="/" aria-label="IQM Docs" target="_blank">
                            <img
                                className="switcher-title-image hover:filter hover:contrast-[.90]"
                                alt="IQM Academy"
                                src={LogoDocs}
                                height={40}
                                width={200}
                            />
                        </a>
                    </div>
                    <div>
                        <a href="https://academy.meetiqm.com" target="_blank" aria-label="IQM Academy">
                            <img
                                className="switcher-title-image hover:filter hover:contrast-[.90]"
                                alt="IQM Academy"
                                src={LogoAcademy}
                                height={40}
                                width={200}
                            />
                        </a>
                    </div>
                    <div>
                        <a
                            href="https://resonance.meetiqm.com"
                            target="_blank"
                            rel="noreferrer"
                            aria-label="IQM Resonance"
                        >
                            <img
                                className="switcher-title-image hover:filter hover:contrast-[.90]"
                                alt="IQM Resonance"
                                src={LogoResonance}
                                height={40}
                                width={200}
                            />
                        </a>
                    </div>
                    <div>
                        <a
                            href="https://support.meetiqm.com"
                            target="_blank"
                            rel="noreferrer"
                            aria-label="IQM Support"
                        >
                            <img
                                className="switcher-title-image hover:filter hover:contrast-[.90]"
                                alt="IQM Support"
                                src={LogoSupport}
                                height={40}
                                width={200}
                            />
                        </a>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AppSwitcher;
