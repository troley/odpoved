/**
 * Enables a graphical loading process animation.
 */
export const enableLoader = (intoElementId) => {
  const loaderElement = document.getElementById(intoElementId);
  loaderElement.innerHTML = `<div class="lds-grid mt-6 h-24"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>`;
};

/**
 * Disables the graphical loading process animation.
 */
export const disableLoader = (fromElementId) => {
  const loaderElement = document.getElementById(fromElementId);
  loaderElement.innerHTML = "";
};
