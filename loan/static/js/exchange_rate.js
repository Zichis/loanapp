$(function () {
  //This didn't work $('.mdb-select').material_select();

  $('#calculateExRateBtn').click(function(){
    let fromCurrency = $('#fromCurrency').val();
    let toCurrency = $('#toCurrency').val();
    let fromAmount = $('#fromAmount').val();
    console.log(fromCurrency);
    console.log(toCurrency);
    console.log(fromAmount);

    $.ajax({
      url: `https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=${fromCurrency}&to_currency=${toCurrency}&apikey=GJYRAMF8Y7MY649Y`, 
      success: function (result) {
        $('#toAmount').html("Processing...");
        console.log(result);
        console.log(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]);

        let exchangeRate = parseFloat(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]);
        let currencyCode = result["Realtime Currency Exchange Rate"]["3. To_Currency Code"];
        fromAmount = parseFloat(fromAmount);

        let toAmount = exchangeRate * fromAmount;

        console.log(toAmount);

        $('#toAmount').html(`${currencyCode} ${toAmount}`);
      }
    });

  });
});