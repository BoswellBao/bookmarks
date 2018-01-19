(function(){
    if(window.myBookmarklet!=undefined){
        myBookmarklet();
    }
    else{
        scr = document.createElement('script');
        scr.src = 'http://mysite.com:8000/static/js/bookmarklet.js?r=' + String(Math.floor(Math.random()*9999999999));
        document.body.appendChild(scr);
    }
})();