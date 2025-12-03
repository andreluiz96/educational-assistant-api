const askButton = document.getElementById("askButton");
const studentIdInput = document.getElementById("studentId");
const questionInput = document.getElementById("question");
const statusEl = document.getElementById("status");
const messagesEl = document.getElementById("messages");

function addMessage(type, text, studentId, questionText) {
  const div = document.createElement("div");
  div.classList.add("msg", type);

  if (type === "user") {
    div.innerHTML = `
      <div class="meta">${studentId || "Aluno"} perguntou:</div>
      <div>${questionText}</div>
    `;
  } else {
    div.innerHTML = `
      <div class="meta">Assistente respondeu:</div>
      <div>${text}</div>
    `;
  }

  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendQuestion() {
  const studentId = studentIdInput.value.trim() || "anon";
  const question = questionInput.value.trim();

  statusEl.classList.remove("error");
  statusEl.textContent = "";

  if (!question) {
    statusEl.classList.add("error");
    statusEl.textContent = "Digite uma pergunta antes de enviar.";
    return;
  }

  addMessage("user", "", studentId, question);

  askButton.disabled = true;
  askButton.textContent = "Perguntando...";
  statusEl.textContent = "Consultando o modelo de IA...";

  try {
    const resp = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ student_id: studentId, question }),
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      throw new Error(err.detail || `Erro HTTP ${resp.status}`);
    }

    const data = await resp.json();
    addMessage("assistant", data.answer, data.student_id, data.question);
    questionInput.value = "";
    statusEl.textContent = "Resposta recebida com sucesso.";
  } catch (err) {
    console.error(err);
    statusEl.classList.add("error");
    statusEl.textContent = "Erro ao processar pergunta. Tente novamente.";
  } finally {
    askButton.disabled = false;
    askButton.textContent = "Perguntar";
  }
}

askButton.addEventListener("click", sendQuestion);
questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
    sendQuestion();
  }
});
