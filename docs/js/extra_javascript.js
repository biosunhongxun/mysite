// 自动更新年份
document.addEventListener("DOMContentLoaded", () => {
  const yearSpan = document.getElementById("year");
  if (yearSpan) {
    const currentYear = new Date().getFullYear();
    yearSpan.textContent = currentYear > 2025 ? `2025-${currentYear}` : "2025";
  }
});