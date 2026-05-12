## BB84 Protocol Simulator

This project was designed while doing my Dissertation on a **'Software Simulation of a BB84 protocol'**

### Project Overview

I decided to use python to code my dissertation, using the sockets and threading library to simulate communication between 2 users: Bob and Alice and then the communication between these 2 users with the presence of an eavesdropper: Eve.

#### How does BB84 protocol work?

The BB84 protocol is the first Quantum Key Distribution (QKD) scheme that allows 2 parties Alice and Bob to communicate securely over a network with a presence of an Eavesdropper. Alice and Bob create a secret key over an insecure channel using bits and basis.

There are 2 basis: Rectilinear (+) and Diagonal (X) basis. *the + represents $\longleftrightarrow\hspace{-21mu}\updownarrow$ and the X represents ${\nearrow\hspace{-18mu}\swarrow}\hspace{-18mu}{\nwarrow\hspace{-18mu}\searrow}$*

Bits to be used: 0 or 1.

These bits are encoded using the basis chosen at random by Alice, and Bob then choses a random set of basis to determine what they think Alice says. 

For example:
- If Alice encodes a bit 0 using a rectilinear basis:$\longleftrightarrow\hspace{-21mu}\updownarrow\hspace{5pt}$ the polarisation will be $\leftrightarrow$ and similarly with a 1: $\updownarrow$
- If Alice encodes a bit 0 using a diagonal basis ${\nearrow\hspace{-18mu}\swarrow}\hspace{-18mu}{\nwarrow\hspace{-18mu}\searrow}$ the polarisation will be: $\nearrow\hspace{-18mu}\swarrow$ and similarly with a 1: $\nwarrow\hspace{-18mu}\searrow$

Bob will chose either basis at random and if any of the basis match, the bits that were used for that basis will be kept and formed into a bit.
Any of the basis that don't match, those bits will be dropped 

Here is a table below demonstrating how it works:
| Step | Data | Bit 1 | Bit 2 | Bit 3 | Bit 4 | Bit 5 | Bit 6 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Alice** | Bit | 0 | 1 | 0 | 1 | 1 | 0 |
| | Basis | $+$ | $\times$ | $+$ | $+$ | $\times$ | $\times$ |
| | Photon | $\leftrightarrow$ | $\nwarrow\kern-11pt\searrow$ | $\leftrightarrow$ | $\updownarrow$ | $\nwarrow\kern-11pt\searrow$ | $\nearrow\kern-11pt\swarrow$ |
| **Bob** | Basis | $+$ | $+$ | $+$ | $\times$ | $\times$ | $\times$ |
| | Measure | $\leftrightarrow$ | $\updownarrow$ | $\leftrightarrow$ | $\nearrow\kern-11pt\swarrow$ | $\nwarrow\kern-11pt\searrow$ | $\nearrow\kern-11pt\swarrow$ |
| **Result** | Sifting | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| | **Key** | **0** | | **0** | | **1** | **0** |

This key here will be used for further communication between Alice and Bob.

#### Dissertation Summary

The project was only created up until this point, while also showing how the presence of an eavesdropper disrupted the key formation process.

Any further details post dissertation will be shown below, and in commits on here.
