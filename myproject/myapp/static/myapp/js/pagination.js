document.addEventListener("DOMContentLoaded", function() {
  const pageLinks = document.querySelectorAll(".list-pages .page-num");

  pageLinks.forEach(link => {
    link.addEventListener("click", function() {
      const page = this.getAttribute("data-page");
      window.location.search = `?page=${page}`;
    });
  });
});