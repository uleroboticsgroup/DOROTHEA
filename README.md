# DOROTHEA

<big>**Do**cker-based f**r**amework f**o**r ga**th**ering n**e**tflow tr**a**ffic</big>

![GitHub Release](https://img.shields.io/github/v/release/uleroboticsgroup/DOROTHEA)
![GitHub License](https://img.shields.io/github/license/uleroboticsgroup/DOROTHEA)


## Description
The primary objective of this framework is to establish an environment that comprehensively monitors and captures all network flows. This is accomplished through the creation of a virtual network and use of Docker containers to run a NetFlow exporter `softflowd` and a collector `nfcaps` to handle the flows.

All interactions within this virtual LAN are captured, parsed, and subsequently exported as IPFIX NetFlows. These NetFlows are stored as nfcaps and are additionally converted into a more user-friendly CSV format, facilitating easier analysis and interpretation.

The **DOROTHEA** project is undergoing a complete restructuring to simplify its architecture and enhance user-friendliness 🚧.

If you are searching for one of the old implementations, we have tagged them as releases.

### Key Objectives

- **Realistic Netflow Generation:** The framework's primary objective is to generate netflows that closely resemble real network traffic. These netflows simulate genuine interactions and transactions, creating a robust dataset for training machine learning models.

- **Malicious Activity Training Data:** The generated netflows are intended for use as training data in the development of models specialized in identifying malicious network activity. This enables the enhancement of security mechanisms and the proactive detection of potential threats.

- **Virtual Network Environment:** By establishing a virtual LAN and deploying containerized nodes, the framework creates a controlled network environment that mimics real-world networking scenarios. This environment facilitates the generation and monitoring of traffic patterns while maintaining a low profile in resource consumption.

- **Effective Monitoring with `softflowd` and `nfcap`:** The framework employs `softflowd` as a netflow exporter and `nfcap` as a netflow collector, enabling comprehensive monitoring of all interactions within the virtual network. This monitoring captures and parses traffic data, exporting it as netflows.


## License
This framework is released under the [LGPL-3.0](LICENSE). Feel free to use, modify, and distribute it in accordance with the terms of the license.

