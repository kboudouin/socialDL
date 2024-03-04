export function toTitleCase(str) {
  return str.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

export function convertDate(inputFormat) {
  const [datePart, timePart] = inputFormat.split(' ');
  const [day, month, year] = datePart.split('/');
  const [hour, minute] = timePart.split(':');
  return Date.UTC(year, month - 1, day, hour, minute);
}

export function convertDateToISO(dateString) {
  const [date, time] = dateString.split(' ');
  const [day, month, year] = date.split('/');
  return `${year}-${month}-${day}T${time}:00`;
}