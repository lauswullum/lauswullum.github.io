window.MathJax = {
  loader: {load: []},
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    packages: ['base', 'ams', 'newcommand', 'noundefined']
  },
  svg: {fontCache: 'local'},
  options: {enableMenu: false}
};
