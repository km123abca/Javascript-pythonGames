function maindestroblock(posx2, posy2, width, height, col) {
  this.posx = posx2;
  this.posy = posy2;
  this.destrolocs = [];
  this.onScreen = true;
  this.hori = parseInt(width / smallblocksize);
  this.vert = parseInt(height / smallblocksize);
  for (var i = -this.vert / 2; i < this.vert / 2; i++)
    for (var j = -this.hori / 2; j < this.hori / 2; j++) {
      this.destrolocs.push(
        new destro(
          this.posx + j * smallblocksize,
          this.posy + i * smallblocksize,
          col
        )
      );
    }
  //	console.log(this.hori+','+this.vert+','+smallblocksize);
  this.dr_w = function () {
    if (!this.onScreen) return false;
    console.log("running");
    var alivecount = 0;
    for (var i in this.destrolocs) {
      if (this.destrolocs[i].onScreen) alivecount += 1;
      else continue;
      this.destrolocs[i].move();
      this.destrolocs[i].dr_w();
    }

    if (alivecount == 0) this.onScreen = false;
  };
}
