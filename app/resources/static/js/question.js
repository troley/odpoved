import { disableLoader, enableLoader } from "./loader.js";

/**
 * Submits the question to get the answer from the server.
 */
const submitQuestionForAnswer = async (e) => {
  e.preventDefault();

  const inputValue = document.getElementById("userQuery").value;

  const data = {
    question: inputValue,
  };

  const answerElemId = "answerToQuestion";

  enableLoader(answerElemId);

  const response = await fetch("/question", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const json = await response.json();
  disableLoader(answerElemId);

  document.getElementById(
    answerElemId
  ).innerHTML = `<div class="rounded bg-zinc-900 border-solid p-6 m-4">
    <p>${json.answer}</p>
  </div
  `;
};

(() => {
  // Form submission
  const form = document.getElementById("questionForm");
  form.addEventListener("submit", submitQuestionForAnswer, true);

  // Bind input to an 'enter' key press event listener, which will submit the answer.
  const input = document.getElementById("userQuery");
  input.addEventListener("keyup", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      submitQuestionForAnswer();
    }
  });
})();
