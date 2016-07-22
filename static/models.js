var oneDayMs = 1000 * 3600 * 24;
var maxAge = 7 * oneDayMs;

function StatusModel(data, width, days, laneHeight) {
    var me = this;
    this.repos = ko.observableArray();
    var i = 0;
    data.forEach(function (repo) {
        me.repos.push(new RepositoryStatusModel(repo, i, width, days, laneHeight));
        i++;
    });
    this.repos.sort(function (left, right) {
       return Math.sign(right.activity() - left.activity());
    });
}

function DayModel(data) {
    var me = this;
    this.name = data.name;
    this.start = Date.parse(data.value);
    this.end = this.start + oneDayMs;
    this.commits = ko.observableArray();
    this.x = data.centre_x;

    this.radius = ko.computed(function () {
        return Math.sqrt(me.commits().length * 100);
    });
    this.count = ko.computed(function () {
        if (me.commits().length > 1) {
            return me.commits().length;
        }
        return "";
    });
    this.contains = function (array, key) {
        for (var i = 0; i < array.length; i++) {
            if (array[i].name == key) {
                return true;
            }
        }
        return false;
    }
    this.contributors = ko.computed(function () {
        var cs = new Array();
        var y = 0;
        me.commits().forEach(function (commit) {
            var author = commit.author();
            if (!me.contains(cs, author)) {
                cs.push({
                    name: author,
                    x: me.x,
                    y: y * 20,
                });
                y++;
            }
        });
        return cs;
    });
}

function RepositoryStatusModel(data, index, width, days, laneHeight) {
    var me = this;
    this.index = ko.observable(index);
    this.uri = ko.observable(data.uri);
    this.name = ko.observable(data.name);
    this.activity = ko.observable(data.activity);
    this.latest = data.latest;
    this.days = ko.observableArray();
    days.forEach(function (day) {
        me.days.push(new DayModel(day));
    });

    this.commits = ko.observableArray();
    if (data.hasOwnProperty('commits')) {
        data.commits.forEach(function (commit) {
            var model = new CommitModel(commit, width);
            model.addTo(me.days);
            me.commits.push(model);
        });
    }

    this.y = ko.computed(function () {
        return me.index() * laneHeight;
    });
    this.translation = ko.computed(function () {
       return "translate(0, " + me.y() + ")";
    });
}
function CommitModel(data, width) {
    var me = this;
    this.id = ko.observable(data.id);
    this.author = ko.observable(data.author);
    this.timestamp = ko.observable(Date.parse(data.timestamp));

    this.age = ko.computed(function () {
        var now = new Date();
        return now.getTime() - me.timestamp();
    })

    this.x = ko.computed(function () {
        var value = (1 - (me.age() / maxAge)) * (width - 200);
        return value;
    });

    this.addTo = function (days) {
        days().forEach(function (day) {
           if (me.timestamp() >= day.start && me.timestamp() < day.end) {
               day.commits.push(me);
           }
        });
    }
}