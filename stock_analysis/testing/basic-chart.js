function Vector(x, y) {
    this.x = x || 0;
    this.y = y || 0;
};

function Chart(width, height, borderX, borderY) {
    this.canvas = document.createElement("canvas");
    this.canvas.width = width;
    this.canvas.height = height;
    this.ctx = this.canvas.getContext("2d");
    this.xaxis = new Vector(0, 1);
    this.yaxis = new Vector(0, 1);
    this.area = new Vector(width - borderX * 2, height - borderY * 2);
    this.border = new Vector(borderX, borderY);
    this.size = new Vector(width, height);
    document.body.appendChild(this.canvas);
}

Chart.prototype.scaledAxis = function (dataset, getter) {
    var first = true;
    var axis = new Vector(0, 0);
    dataset.forEach(function (pt) {
        var v = getter(pt);
        if (first) {
            first = false;
            axis.x = v;
            axis.y = v;
        } else {
            if (v < axis.x) {
                axis.x = v;
            } else if (v > axis.y) {
                axis.y = v;
            }
        }
    });
    axis.y -= axis.x;
    return axis;
};

Chart.prototype.scaleAxisX = function (dataset, getter) {
    this.xaxis = this.scaledAxis(dataset, getter);
    return this;
};

Chart.prototype.scaleAxisY = function (dataset, getter) {
    this.yaxis = this.scaledAxis(dataset, getter);
    return this;
};

Chart.prototype.scalePoint = function (pt) {
    return new Vector(
        (1 - ((pt.x - this.xaxis.x) / this.xaxis.y)) * this.area.x + this.border.x, 
        (1 - ((pt.y - this.yaxis.x) / this.yaxis.y)) * this.area.y + this.border.y
    );
};

Chart.prototype.plotLine = function (dataset, getter) {
    var self = this;
    var first = true;
    this.ctx.beginPath();
    dataset.forEach(function (d) {
        var pt = self.scalePoint(getter(d));
        if (first) {
            first = false;
            self.ctx.moveTo(pt.x, pt.y);
        } else {
            self.ctx.lineTo(pt.x, pt.y);
        }
    });
    this.ctx.stroke();
    return this;
};