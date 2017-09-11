var app = angular.module('IPLapp',[])
.config(function($interpolateProvider) {
         $interpolateProvider.startSymbol('[[').endSymbol(']]');
                          });

//main controller starts
app.controller('mainCtrl',MainController);
function MainController($scope , boolFactory ,dbFactory){
    $scope.boolFactory = boolFactory;
    $scope.dbFactory = dbFactory;
    

    $scope.change = function(item){
        boolFactory.getViewNames(item);
        dbFactory.getCompletedData(item)
        
    }

}
//main controller ends

//home controller starts
app.controller('homeCtrl',HomeController);
function HomeController($scope , boolFactory){
$scope.boolFactory = boolFactory;
$scope.aa = boolFactory.home;

}
//home controller ends

//live controller starts
app.controller('liveCtrl',LiveController);
function LiveController($scope , boolFactory , dbFactory){
$scope.boolFactory = boolFactory;
$scope.dbFactory = dbFactory;
$scope.data = null;


    $scope.reloadPage = function(item){
        dbFactory.getCompletedData('live')
        for(i=0;i<dbFactory.length;i++){
            if(dbFactory[i].matchdesc == item.matchdesc){
                $scope.data = dbFactory[i]
            }
        }
    }


    $scope.scorecard = function(data){
        $scope.data = data;
        boolFactory.getViewNames('scorecard');
    }

}
//live controller ends


//preview controller starts
app.controller('previewCtrl',PreviewController);
function PreviewController($scope , boolFactory , dbFactory){
    $scope.boolFactory = boolFactory;
    $scope.dbFactory = dbFactory;
}
//preview controller ends


//result controller starts
app.controller('resultCtrl',ResultController);
function ResultController($scope , boolFactory , dbFactory ){
    $scope.boolFactory = boolFactory;
    $scope.dbFactory = dbFactory;
}
//result controller ends

//bool factory starts
app.factory('boolFactory',BoolFactory);
    function BoolFactory(){
    
    var viewNames = {
       'home' : true,
       'live' : false,
       'preview' : false,
       'result' : false,
       'refresh':false,
       'scorecardBool':false
};

    
   
    viewNames.getViewNames = function(arg){
    if(arg=="home")
        {viewNames.home=true}
        else
        {viewNames.home=false;}
        
        if(arg=="live")
        {
            viewNames.live=true;
            viewNames.refresh=false;
            viewNames.scorecardBool=false;

        }
        else
        {viewNames.live=false;}
        
        if(arg=="preview")
        {viewNames.preview=true;}
        else
        {viewNames.preview=false;}
        
        if(arg=="result")
        {
            viewNames.result=true;
        }
        else
        {viewNames.result=false;}
        if(arg=="scorecard")
        {
            viewNames.live=true;
            viewNames.refresh=true;
            viewNames.scorecardBool=true;

        }
        else
        {viewNames.refresh=false;}
    }
    
 
    return viewNames
  }
    //bool factory ends

app.factory('dbFactory',DBFactory);


function DBFactory($http){

    var matchData = []; 


    matchData.getCompletedData = function(item){
        if(item=='result'){
            $http({
                method : 'POST',
                url : '/getCompletedData',
            })
            .then(
                function(response){
                    angular.copy(response.data, matchData);
                }
                ,function(error){
                    alert(error)
            });
        }
        if(item=='preview'){
            $http({
                method : 'POST',
                url : '/getPreviewData',
            })
            .then(
                function(response){
                    angular.copy(response.data, matchData);
                }
                ,function(error){
                    alert(error)
            });
        }
        if(item=='live'){
            $http({
                method : 'POST',
                url : '/getLiveData',
            })
            .then(
                function(response){
                    angular.copy(response.data, matchData);
                    x = response.data
                    
                }
                ,function(error){
                    alert(error)
            });
        }
   };

   return matchData;
    

    
}