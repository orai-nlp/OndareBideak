 // In a perfect world, this would be its own library file that got included
    // on the page and only the ``$(document).ready(...)`` below would be present.
    // But this is an example.
    var Autocomplete = function(options) {
      this.form_selector = options.form_selector
      this.url = options.url || '/autocomplete/'
      this.delay = parseInt(options.delay || 300)
      this.minimum_length = parseInt(options.minimum_length || 3)
      this.form_elem = null
      this.query_box = null
    }

    Autocomplete.prototype.setup = function() {
      var self = this

      this.form_elem = $(this.form_selector)
      this.query_box = this.form_elem.find('input[name=search_input]')

      // Watch the input box.
      this.query_box.on('keyup', function() {
        var query = self.query_box.val()

        if(query.length < self.minimum_length) {
          return false
        }

        self.fetch(query)
      })

	 //MADDALEN : HAU KOMENTATU DUT KLIKATZEAN AUKERATUTAKO ITEMERA JOATEKO, bILAKETA KUTXAN IDATZI BEHARREAN
      // On selecting a result, populate the search field.
      /*this.form_elem.on('click', '.ac-result', function(ev) {
        self.query_box.val($(this).text())
        $('.ac-results').remove()
        return false
      })*/
    }

    Autocomplete.prototype.fetch = function(query) {
      var self = this

      $.ajax({
    	method: 'GET',  
        url: this.url,
        dataType : 'html',
        data: {
          'q': query
          
        },
        success: function(data) {
          self.show_results(data)          
        }
      })
    }

    Autocomplete.prototype.show_results = function(data) {
      // Remove any existing results.
      //$('.ac-results').remove();
      //$('.ac-result').remove();
      $('#autocomplete-container').empty();
      $('#autocomplete-container').html(data);
      var itm = document.getElementById('autocomplete_items'); 
      var pth = document.getElementById('autocomplete_paths');
      if (itm || pth){
          $('#autocomplete-div').show();    	  
      }
      else{
    	  $('#autocomplete-div').hide();
      }

    }

    
    
    $(document).ready(function() {
      window.autocomplete = new Autocomplete({
        form_selector: '.autocomplete-me'
      })
      window.autocomplete.setup()
    })
    
    $(document).ready(function() {
      window.autocomplete = new Autocomplete({
        form_selector: '.autocomplete-me-2'
      })
      window.autocomplete.setup()
    })
