import { disableLoader, enableLoader } from "./loader.js";

let formData = { name: null, content: null };

/**
 * Process the chosen file into blob and store the contents in formData.
 */
const handleFile = (that) => {
  const file = that.target.files[0];

  const fileReader = new FileReader();
  fileReader.addEventListener(
    "load",
    () => {
      formData.file = fileReader.result;

      formData = {
        name: file.name,
        content: fileReader.result,
      };
    },
    false
  );

  if (file) {
    fileReader.readAsDataURL(file);
  }
};

/**
 * Processes the submission of the chosen file to the server.
 */
const formSubmit = async (e) => {
  e.preventDefault();

  const loaderElemId = "loader";

  if (formData.name === null || formData.content === null) {
    alert("Vyberte prosím súbor (PDF).");
    return;
  }

  enableLoader(loaderElemId);

  const response = await fetch("/save_file", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  if (response.ok) {
    window.location.replace(window.location.origin);
  } else if (!response.ok) {
    alert(JSON.stringify(await response.json()));
  }
  disableLoader(loaderElemId);
};

(() => {
  // Process chosen file data
  const inputElement = document.getElementById("fileToUpload");
  inputElement.addEventListener("change", handleFile, false);

  // Form submission
  const form = document.getElementById("fileUploadForm");
  form.addEventListener("submit", formSubmit, true);
})();
