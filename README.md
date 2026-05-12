# BB84 Protocol Simulator

This project was developed as part of my dissertation: **"Software Simulation of the BB84 Protocol."**

## Project Overview

I used **Python** to build this simulation, leveraging the `sockets` and `threading` libraries to facilitate communication between two users, **Alice** and **Bob**. The project also simulates the impact of an eavesdropper, **Eve**, on the quantum channel to demonstrate how QKD detects intrusion.

## How the BB84 Protocol Works

The BB84 protocol is the first Quantum Key Distribution (QKD) scheme. It allows two parties to create a shared secret key over an insecure channel. Alice and Bob use random bit strings and random bases to encode and decode information.

### 1. The Bases
There are two bases used for polarization. To represent these in a digital environment, we map them as follows:

*   **Rectilinear Basis ($+$):** Composed of Horizontal ($\leftrightarrow$) and Vertical ($\updownarrow$) orientations.
*   **Diagonal Basis ($\times$):** Composed of 45° ($\nearrow\kern-10pt\swarrow$) and 135° ($\nwarrow\kern-10pt\searrow$) orientations.

### 2. Encoding Logic
Alice chooses a random bit (**0** or **1**) and a random basis to determine the polarization of the photon sent.

| Bit | Rectilinear ($+$) | Diagonal ($\times$) |
| :--- | :---: | :---: |
| **0** | $\leftrightarrow$ | $\nearrow\kern-10pt\swarrow$ |
| **1** | $\updownarrow$ | $\nwarrow\kern-10pt\searrow$ |

### 3. Key Exchange Simulation
Bob chooses his own bases at random to measure Alice's photons. If their bases match, the bit is kept. If they don't, the bit is discarded (sifted).

| Participant | Property | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Alice** | **Key bit** | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| | **Basis** | $+$ | $\times$ | $+$ | $+$ | $\times$ | $\times$ | $+$ |
| | **Photon** | $\leftrightarrow$ | $\nwarrow\kern-10pt\searrow$ | $\updownarrow$ | $\leftrightarrow$ | $\nearrow\kern-10pt\swarrow$ | $\nwarrow\kern-10pt\searrow$ | $\leftrightarrow$ |
| **Bob** | **Basis** | $\times$ | $\times$ | $+$ | $\times$ | $\times$ | $+$ | $+$ |
| | **Measure** | $\nearrow\kern-10pt\swarrow$ | $\nwarrow\kern-10pt\searrow$ | $\updownarrow$ | $\nwarrow\kern-10pt\searrow$ | $\nearrow\kern-10pt\swarrow$ | $\updownarrow$ | $\leftrightarrow$ |
| **Result** | **Sifting** | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| **Final Key** | | | **1** | **1** | | **0** | | **0** |

This final sifted key can then be used for encrypted communication using algorithms like AES or One-Time Pad.

## Dissertation Summary

The project demonstrates the core QKD process and illustrates how the presence of an eavesdropper (**Eve**) introduces errors. Because Eve cannot measure a photon without collapsing its state, her presence increases the **Quantum Bit Error Rate (QBER)**, which Alice and Bob detect during the public parity check, alerting them to the intrusion.

Any further details post-dissertation will be shown below and in the repository commits.
