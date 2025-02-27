(function($) {

  'use strict';

  /*--------------------------------------------------------------
    ## Scripts initialization
  --------------------------------------------------------------*/

  $(window).on('load', function() {
    $(window).trigger('scroll');
    $(window).trigger('resize');
    preloaderSetup();
  });

  $(document).on('ready', function() {
    $(window).trigger('resize');
    primaryMenuSetup();
    mobileMenu();
    onePage();
  });

  $(window).on('resize', function() {
    mobileMenu();
  });

  $(window).on('scroll', function() {
    scrollFunction();
  });

  $.exists = function(selector) {
    return ($(selector).length > 0);
  }

  /*--------------------------------------------------------------
    ## Preloader
  --------------------------------------------------------------*/
  function preloaderSetup() {
    $(".st-preloader-wave").fadeOut();
    $("#st-preloader").delay(150).fadeOut("slow");
  }
  /*--------------------------------------------------------------
    ## Primary Menu
  --------------------------------------------------------------*/

  function primaryMenuSetup() {

    $('.st-main-nav').before('<div class="st-m-menu-btn"><span></span></div>');
    $('.st-m-menu-btn').on('click', function() {
      $(this).toggleClass('st-m-menu-btn-ext');
      $(this).siblings('.st-main-nav').slideToggle('slow');
    });

    $('.menu-item-has-children ').append('<i class="st-plus st-dropdown"></i>');
    $('.st-dropdown').on('click', function() {
      $(this).prev().slideToggle('slow');
      $(this).toggleClass('st-plus st-minus')
    });
    // Mega Menu
    $('.st-mega-wrapper>li>a').removeAttr("href");
    $('.st-mega-wrapper>li>a').on('click', function() {
      $(this).siblings().slideToggle();
      $(this).toggleClass('st-megamenu-plus');
    });

    $('.st-solid-header.st-sticky-header').before('<div class="st-solid-header-height"></div>');

    if ($.exists('.st-header-style13 .st-promotion-bar')) {
      $('.st-header-style13').addClass('st-remove-header-padding');
    }

  }

  function mobileMenu() {

    if ($(window).width() <= 991) {
      $('.st-primary-nav').addClass('st-m-menu').removeClass('st-primary-nav');
      $('.st-profile-toggle').addClass('st-offset-menu');
    } else {
      $('.st-m-menu').addClass('st-primary-nav').removeClass('st-m-menu');
      $('.st-profile-toggle').removeClass('st-offset-menu');
    }
    var solidHeaderHight = $('.st-solid-header').height() + 'px';
    $('.st-solid-header-height').css('height', solidHeaderHight);

    // Transparent Header page
    var pageHeadingPad = (($('.st-site-header').height()) + 45) + 'px'
    $('.st-transparent-header+.st-page-heading-wrap').css('padding-top', pageHeadingPad);
    // Header Promo Bar
    var reduseSolidHeaderHight = (($('.st-solid-header').height()) - ($('.st-promotion-bar').height())) + 'px';
    var redusePageHeadingPad = (($('.st-site-header').height()) - ($('.st-promotion-bar').height()) + 45) + 'px';
    $('.st-promotion-cross').on('click', function() {
      $(this).parents('.st-promotion-bar').slideUp(400);
      $(this).parents('.st-site-header').siblings('.st-solid-header-height').css('height', reduseSolidHeaderHight);
    });
    $('.st-transparent-header .st-promotion-cross').on('click', function() {
      $('.st-page-heading-wrap').css('padding-top', redusePageHeadingPad);
    });

  }

  /*--------------------------------------------------------------
    ## Scroll Function
  --------------------------------------------------------------*/

  function scrollFunction() {

    var scroll = $(window).scrollTop();
    // For Small Header
    if (scroll >= 10) {
      $('.st-site-header').addClass('small-height');
    } else {
      $('.st-site-header').removeClass('small-height');
    }

  }

  /*--------------------------------------------------------------
    ## one page
  --------------------------------------------------------------*/
  function onePage() {
    // Smoth Animated Scroll
    $('.smoth-scroll').on('click', function() {
      var thisAttr = $(this).attr('href');
      if ($(thisAttr).length) {
        var scrollPoint = $(thisAttr).offset().top;
        $('body,html').animate({
          scrollTop: scrollPoint
        }, 600);
      }
      return false;
    });
  }

})(jQuery); // End of use strict
