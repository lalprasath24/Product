(function() {
  // Prevent multiple loads
  if (window.RemoWidgetLoaded) return;
  window.RemoWidgetLoaded = true;

  // Load the widget script
  const script = document.createElement('script');
  script.src = 'https://your-domain.com/remo-widget.js'; // Replace with your CDN URL
  script.async = true;
  
  // Load CSS
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'https://your-domain.com/remo-widget.css'; // Replace with your CDN URL
  
  document.head.appendChild(link);
  document.head.appendChild(script);
})();