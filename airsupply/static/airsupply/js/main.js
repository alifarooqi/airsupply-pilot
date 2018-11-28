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

		$('.cart_quantity_up').click((e)=>{
			let $target = $(e.target);
            let input = $target.next("input");
            var currentVal = parseInt(input.val());
            input.val(currentVal + 1);
		});
		$('.cart_quantity_down').click((e)=>{
			let $target = $(e.target);
            let input = $target.prev("input");
            var currentVal = parseInt(input.val());
            if (currentVal > 0)
            	input.val(currentVal - 1);
		});
	}
};

let TogglePriorityQueue = {
    init: function() {
        $(".item-details").find(".toggleWrapper").hide();
		this.bindEvents();
	},
    bindEvents: function(){
        $("#priority-list-table").click(function(event) {
            let $target = $(event.target);
            if ( $target.closest("td").attr("colspan") > 1) {
                // $target.slideUp();
            }
            else if($target.prop("tagName") == "BUTTON"){
            	$target.closest("tr").find(".expandCollapseIcon").children().first().addClass(" glyphicon-minus-sign")
                $target.closest("tr").next().find(".toggleWrapper").slideDown();
            	$target.closest("tr").next().find(".order-processed-btn").slideDown("fast");
            	$target.closest("tr").next().find(".down-shipping-btn").slideDown("fast");
            	$target.prop("disabled",true);
            	$target.closest("tr").addClass("active-process")
            	$target.closest("tr").next().addClass("active-process")
				let order_id = $target.closest("tr").find(".cart_description").text().trim()
				let url = "1/" + order_id;
				$.getJSON(url, function(result){});
			}
			else {
            	$target.closest("tr").find(".expandCollapseIcon").children().first().toggleClass(" glyphicon-minus-sign")
                $target.closest("tr").next().find(".toggleWrapper").slideToggle();
            }
        });
    }
}

/*scroll to top*/

$(document).ready(function(){

	BrowsePage.init();
	TogglePriorityQueue.init();
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
