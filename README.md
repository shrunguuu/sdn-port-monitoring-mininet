##  Problem Statement

This project demonstrates a Software Defined Networking (SDN) environment using **Mininet** and a **POX controller**.
The goal is to implement controller-based network behavior using OpenFlow, and analyze connectivity, failures, and performance.

---

## The Objective

* Simulate a network using Mininet
* Use POX controller to manage traffic
* Demonstrate:

  * Normal communication
  * Link failure behavior
  * Recovery after failure
  * Performance using iperf

---

## Network Topology

* 1 Switch (s1)
* 3 Hosts (h1, h2, h3)

---

## Setup & Execution

###  Step 1: Start POX Controller

```bash
cd pox
./pox.py forwarding.l2_learning
```

---

###  Step 2: Run Mininet Topology

```bash
sudo mn --controller=remote,port=6633 --topo=single,3
<img width="601" height="532" alt="topo" src="https://github.com/user-attachments/assets/797d76ee-5ca7-44fc-a4d6-710feaf752b3" />



---

##  Functional Demonstration

### 1. Initial Connectivity Test

All hosts can communicate successfully.

<img width="515" height="153" alt="initial" src="https://github.com/user-attachments/assets/f43c916c-8e08-4b53-8b3b-31380dda9a34" />


✔ Result:

* 0% packet loss
* Full connectivity

---

### 2. Link Failure Simulation

Command used:

```bash
link s1 h1 down
pingall
```
<img width="595" height="200" alt="linkfail" src="https://github.com/user-attachments/assets/d0bb6487-72e4-4126-9445-4a04ed9a0a0f" />


✔ Observation:

* Communication involving h1 fails
* Packet loss increases (66%)

---

### 3. Controller Detection (POX Logs)

Controller detects link failure.
<img width="591" height="205" alt="linkrecovery" src="https://github.com/user-attachments/assets/99388db1-3671-4a4a-98d8-f66b34477ee3" />
<img width="595" height="200" alt="pox logs" src="https://github.com/user-attachments/assets/5bccadde-e168-4258-ab0a-e1048e983e60" />


✔ Observation:

* Port status changes to DOWN
* Controller logs packet activity

---

### 4. Link Recovery

Command used:

```bash
link s1 h1 up
pingall
```

<img width="591" height="205" alt="linkrecovery" src="https://github.com/user-attachments/assets/482f2425-6c26-46f5-9ad3-52d38a344bec" />


✔ Result:

* Connectivity restored
* 0% packet loss

---

### 5. Controller Detection (Recovery)

<img width="685" height="298" alt="pox logs after recovery" src="https://github.com/user-attachments/assets/c21bc61d-a8b5-483e-8127-05e036317589" />


✔ Observation:

* Port status changes to UP
* Network resumes normal operation

---

###  6. Performance Testing using iperf

Commands:

```bash
h3 iperf -s &
h1 iperf -c h3
```
<img width="985" height="357" alt="iperf" src="https://github.com/user-attachments/assets/eacfc63c-8321-41bb-9574-b08ef09f4670" />


✔ Result:

* High throughput achieved (~58 Gbits/sec)
* Confirms efficient data transfer

---

##  SDN Logic Explanation

* POX controller acts as a **learning switch**
* It handles **packet_in events**
* Dynamically installs flow rules:

  * Match: MAC address
  * Action: Forward to correct port

---

##  Observations

| Scenario    | Result               |
| ----------- | -------------------- |
| Normal      | Full connectivity    |
| Link Down   | Packet loss observed |
| Link Up     | Network restored     |
| Performance | High throughput      |

---

##  Conclusion

This project successfully demonstrates:

* Controller-based traffic management
* Dynamic flow rule installation
* Network failure handling
* Performance measurement


