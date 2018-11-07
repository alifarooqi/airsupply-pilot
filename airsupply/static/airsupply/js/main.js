/*price range*/

 $('#sl2').slider();

	var RGBChange = function() {
	  $('#RGB').css('background', 'rgb('+r.getValue()+','+g.getValue()+','+b.getValue()+')')
	};

var BrowsePage = {
	init: function() {
		this.$container = $('.features_items');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.add-to-cart', this.$container).on('click', function(e) {
			e.preventDefault();
			var self = $(this);
			var qty = $(this).parents('form:first')[0][1].value;
            var itemID = $(this).parents('form:first')[0][2].value;
            var url = '../cart/add/?itemid=' + itemID + '&qty=' + qty;
            console.log(url, itemID, qty);
			$.getJSON(url, function(result) {
				console.log(result)
				if (result.success) {
					alert("Added to the Cart!");
				}
				else if (result.error_message)
					alert("Error: " + result.error_message);
				else
					alert("Unexpected error: Check your cart!")
			});

			return false;
		});
	}
};

/*scroll to top*/

$(document).ready(function(){

	BrowsePage.init();
	$(function () {
		$.scrollUp({
	        scrollName: 'scrollUp', // Element ID
	        scrollDistance: 300, // Distance from top/bottom before showing element (px)
	        scrollFrom: 'top', // 'top' or 'bottom'
	        scrollSpeed: 300, // Speed back to top (ms)
	        easingType: 'linear', // Scroll to top easing (see http://easings.net/)
	        animation: 'fade', // Fade, slide, none
	        animationSpeed: 200, // Animation in speed (ms)
	        scrollTrigger: false, // Set a custom triggering element. Can be an HTML string or jQuery object
					//scrollTarget: false, // Set a custom target element for scrolling to the top
	        scrollText: '<i class="fa fa-angle-up"></i>', // Text for element, can contain HTML
	        scrollTitle: false, // Set a custom <a> title if required.
	        scrollImg: false, // Set true to use image
	        activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
	        zIndex: 2147483647 // Z-Index for the overlay
		});
	});
});
