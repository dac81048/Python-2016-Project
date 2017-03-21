var timepicker = new Pikaday({
    field: document.getElementById('start_date'),
    firstDay: 1,
    minDate: new Date(2016, 0, 1),
    maxDate: new Date(2100, 12, 31),
    yearRange: [2016,2100],
    showTime: true,
    autoClose: false,
    use24hour: false,
    format: 'MMM Do YYYY, h:mm a'
});