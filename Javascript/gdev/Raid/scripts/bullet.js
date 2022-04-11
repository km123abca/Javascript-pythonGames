function bullet(posx2, posy2, wid, hei, ang) {
  this.posx = posx2;
  this.posy = posy2;
  this.width = wid;
  this.height = hei;
  this.img = new Image();
  this.img.src = "./sprites/Fire.png";
  this.rotangle = ang;

  this.onScreen = true;

  this.vel = 18 * xx;
  this.velx = this.vel * Math.cos((ang / 180) * Math.PI);
  this.vely = this.vel * Math.sin((ang / 180) * Math.PI);

  this.xpts = [
    -this.width / 2,
    this.width / 2,
    this.width / 2,
    -this.width / 2,
  ];
  this.ypts = [
    -this.height / 2,
    -this.height / 2,
    this.height / 2,
    this.height / 2,
  ];

  this.dr_w = function () {
    if (!this.onScreen) return false;
    ctx.save();
    ctx.translate(this.posx - camx, this.posy - camy);
    ctx.rotate((this.rotangle * Math.PI) / 180);
    ctx.drawImage(
      this.img,
      -this.width / 2,
      -this.height / 2,
      this.width,
      this.height
    );

    ctx.restore();
  };
  this.dr_w_old = function () {
    if (!this.onScreen) {
      console.log("refused to draw ");
      return false;
    }
    console.log("drawing");
    ctx.save();
    ctx.translate(this.posx - camx, this.posy - camy);
    ctx.rotate((this.ang / 180) * Math.PI);

    ctx.fillStyle = "#00FFFF";
    ctx.strokeStyle = "#000000";
    ctx.beginPath();
    ctx.moveTo(this.xpts[0], this.ypts[0]);
    for (var g = 1; g < this.xpts.length; g++)
      ctx.lineTo(this.xpts[g], this.ypts[g]);
    ctx.closePath();
    ctx.stroke();
    ctx.fill();

    ctx.restore();
  };
  this.move = () => {
    if (!this.onScreen) return false;
    this.posx += this.velx;
    this.posy += this.vely;
    //console.log(this.posx+','+this.posy);
    this.wallCheck();
    this.destroyHostiles();
    // console.log(this.velx + "," + this.vely);
  };

  this.wallCheck = () => {
    if (
      this.posx - camx > canvas.width ||
      this.posx - camx < 0 ||
      this.posy - camy > canvas.height ||
      this.posy - camy < 0
    ) {
      this.onScreen = false;
      console.log("bullet out");
    }
  };

  this.destroyHostiles = () => {
    // return false;
    for (var h of hostiles) {
      if (!h.onScreen) continue;
      if (collisioncheckz(this, h)) {
        if (h.hits < h.resil) {
          h.hits += 1;
          // console.log("fdfdf:" + h.vely);
          h.vely += 2 * yy;
          // console.log(h.vely);
          this.onScreen = false;
          console.log("bullet out");
          return false;
        }
        this.onScreen = false;
        // h.onScreen = false;
        // simulateDestruction(h, "#FFFF00");
        h.destroySelf();
      }
    }
  };
}
