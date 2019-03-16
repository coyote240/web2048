angular.module('web2048', [])
.directive('game', function () {
    return {
        link: function (scope, element, attrs) {
            var start = attrs.start;
            scope.getTurn(start);
        },
        controller: ['$scope', 'TurnService', function ($scope, TurnService) {
            $scope.states = [];

            $scope.getTurn = function (start) {
                TurnService.getBoard(start)
                    .then(function (response) {
                        $scope.states.push(response.data);
                    });
            };
        }]
    };
})
.directive('turn', function () {
    return {
        scope: {
            state: '='
        },
        templateUrl: '/static/js/turn.html',
        controller: ['$scope', function ($scope) {
        }]
    };
})
.factory('TurnService', ['$http', function ($http) {
    return {
        getBoard: function (id) {
            return $http({
                method: 'GET',
                url: '/turn/' + id
            });
        }
    };
}]);
