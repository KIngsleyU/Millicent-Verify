const form = document.getElementById("slope-form");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  resultEl.textContent = "";
  errorEl.textContent = "";

  // Collect the three numbers from the form.
  const y = [document.getElementById("y1"), document.getElementById("y2"), document.getElementById("y3")].map(
    (input) => parseFloat(input.value)
  );

  // Quick validation.
  if (y.some((val) => Number.isNaN(val))) {
    errorEl.textContent = "Please enter three valid numbers.";
    return;
  }

  try {
    const response = await fetch("http://localhost:5050/slope", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ y }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error || "Server error");
    }

    const data = await response.json();
    resultEl.textContent = `Slope: ${data.slope}`;
  } catch (err) {
    errorEl.textContent = err.message || "Request failed";
  }
});

