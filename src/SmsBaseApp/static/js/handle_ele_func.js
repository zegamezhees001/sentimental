/**
 *
 * @param {*} eleName
 * @param {*} className
 * @param {*} textInput
 * @param {*} funcOnclick is function when click
 */
function createElementFun(eleName, className, textInput, funcOnclick) {
  const createElement = document.createElement(eleName);
  if (textInput) {
    const createTextNode = document.createTextNode(textInput);
    createElement.appendChild(createTextNode);
  }
  if (className) createElement.className = className;
  if (funcOnclick) createElement.onclick = funcOnclick;
  return createElement;
}

/**
 *
 * @param {*} element element is cleared.
 */
function removeChild(element) {
  while (element.firstChild) {
    element.firstChild.remove();
  }
}
