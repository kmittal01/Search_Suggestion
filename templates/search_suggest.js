function search_suggest () {

  search_suggest.prototype.insert=function(json_string,callback) {
  var serializedData2 ='json_string='+json_string;
  $.ajax({
    type: 'post',
    url: 'http://localhost:8002/insert',
    data: serializedData2,
    async:true,
    success: callback,
    error: function(XMLHttpRequest, textstatus, error) { 
        console.log(error);         
      }
  });
}  

search_suggest.prototype.search=function(prefix,callback) {
   var serializedData2 ='prefix='+prefix;
  $.ajax({
    type: 'post',
    url: 'http://localhost:8002/search',
    data: serializedData2,
    async:true,
    success: callback,
    error: function(XMLHttpRequest, textstatus, error) { 
        console.log(error);         
      }
  });
 }

}