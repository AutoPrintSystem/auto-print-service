
function getCurrentDate() {
    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const day = now.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    const currentDate = getCurrentDate();
    const printDateInput = document.querySelector('[name="print_date"]');
    printDateInput.min = currentDate;
  });
  
