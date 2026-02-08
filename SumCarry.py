import streamlit as st
import cirq
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="4-bit Quantum Adder", layout="centered")

st.title("⚛️ 4-Bit Quantum Ripple Carry Adder")

st.markdown("Add two 4-bit numbers using a quantum ripple carry structure.")

# -----------------------------
# INPUT SECTION
# -----------------------------
a_input = st.number_input("Enter 4-bit number A (0-15)", 0, 15, 3)
b_input = st.number_input("Enter 4-bit number B (0-15)", 0, 15, 5)

# Convert to binary
A_bits = [(a_input >> i) & 1 for i in range(4)]
B_bits = [(b_input >> i) & 1 for i in range(4)]

st.subheader("Binary Representation")
st.write("A:", A_bits[::-1])
st.write("B:", B_bits[::-1])

# -----------------------------
# QUANTUM REGISTERS
# -----------------------------
A = [cirq.NamedQubit(f"A{i}") for i in range(4)]
B = [cirq.NamedQubit(f"B{i}") for i in range(4)]
C = [cirq.NamedQubit(f"C{i}") for i in range(5)]

circuit = cirq.Circuit()

# Initialize qubits
for i in range(4):
    if A_bits[i] == 1:
        circuit.append(cirq.X(A[i]))
    if B_bits[i] == 1:
        circuit.append(cirq.X(B[i]))

# -----------------------------
# RIPPLE CARRY ADDER
# -----------------------------
for i in range(4):
    circuit.append(cirq.CCNOT(A[i], B[i], C[i+1]))
    circuit.append(cirq.CNOT(A[i], B[i]))
    circuit.append(cirq.CCNOT(C[i], B[i], C[i+1]))
    circuit.append(cirq.CNOT(C[i], B[i]))

# Measure results
for i in range(4):
    circuit.append(cirq.measure(B[i], key=f"S{i}"))
circuit.append(cirq.measure(C[4], key="Carry"))

st.subheader("Quantum Circuit")
st.image("adder.png")

# -----------------------------
# RUN SIMULATION
# -----------------------------
sim = cirq.Simulator()
result = sim.run(circuit, repetitions=1)

# Extract results
sum_bits = [result.measurements[f"S{i}"][0][0] for i in range(4)]
carry_out = result.measurements["Carry"][0][0]

sum_decimal = sum([bit << i for i, bit in enumerate(sum_bits)]) + (carry_out << 4)

st.subheader("Result")
st.success(f"Sum (binary): {sum_bits[::-1]}  | Carry: {carry_out}")
st.success(f"Sum (decimal): {sum_decimal}")

# -----------------------------
# VISUALIZATION
# -----------------------------
fig, ax = plt.subplots()

labels = ["A", "B", "Result"]
values = [a_input, b_input, sum_decimal]

ax.bar(labels, values)
ax.set_ylabel("Decimal Value")
ax.set_title("4-bit Quantum Addition")

st.pyplot(fig)

st.markdown("""
### 🔬 How It Works
- Uses Toffoli (CCNOT) gates to generate carry.
- Uses CNOT gates for XOR (sum).
- Carry ripples from LSB to MSB.
- Final carry stored in C4.
""")
st.markdown(f""">Developed by Mounesh C Badiger""")