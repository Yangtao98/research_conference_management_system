

  /**
   * Animation on scroll function and init
   */
  function aos_init() {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', () => {
    aos_init();
  });



  jQuery(function() {
    jQuery('.reply-btn').click(function() {
      jQuery('#reviwerComment' + $(this).attr('target')).show();
    });

    jQuery('.close-reply').click(function() {
      jQuery('#reviwerComment' + $(this).attr('target')).hide();
    });


    jQuery('.edit-btn').click(function() {
      jQuery('#input' + $(this).attr('target')).show();
      jQuery('#save' + $(this).attr('target')).show();
      jQuery('#cancel' + $(this).attr('target')).show();
      jQuery('#edit' + $(this).attr('target')).hide();
      jQuery('#delete' + $(this).attr('target')).hide();
      jQuery('#p' + $(this).attr('target')).hide();
    });

    jQuery('.cancel-btn').click(function() {
      jQuery('#input' + $(this).attr('target')).hide();
      jQuery('#save' + $(this).attr('target')).hide();
      jQuery('#cancel' + $(this).attr('target')).hide();
      jQuery('#edit' + $(this).attr('target')).show();
      jQuery('#delete' + $(this).attr('target')).show();
      jQuery('#p' + $(this).attr('target')).show();
    });
  });
