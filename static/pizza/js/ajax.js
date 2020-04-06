add_to_cart = function(item_id){
    $.get('/add_to_cart/',{'item_id':item_id,},function(data){
        console.log(data);
        $('#add_to_cart').html(data);
    });
};