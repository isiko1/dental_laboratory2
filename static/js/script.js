$(document).ready(function(){
        $(".collapsible").collapsible();
        $("select").material_select();
        $(".sidenav").sidenav();
         M.updateTextFields();
      });
      /* ----Code from mini project------*/
      $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 100, // Creates a dropdown of 80 years to control year,
        today: "Today",
        clear: "Clear",
        close: "Ok",
        closeOnSelect: false, // Close upon selecting a date,
      });