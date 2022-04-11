function bomb(posx2, posy2) {
  this.posx = posx2;
  this.posy = posy2;
  this.width = 10;
  this.height = 10;

  this.onScreen = true;
  this.hooked = false;

  this.velx = 0;
  this.vely = 8 * yy;

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
  this.img = new Image();
  this.img.src = "./sprites/Fire.png";

  this.dr_w = function () {
    if (!this.onScreen) return false;

    ctx.save();
    ctx.translate(this.posx - camx, this.posy - camy);

    // ctx.fillStyle = "#FF0000";
    // ctx.strokeStyle = "#000000";
    // ctx.beginPath();
    // ctx.moveTo(this.xpts[0], this.ypts[0]);
    // for (var g = 1; g < this.xpts.length; g++)
    //   ctx.lineTo(this.xpts[g], this.ypts[g]);
    // ctx.closePath();
    // ctx.stroke();
    // ctx.fill();

    ctx.drawImage(
      this.img,
      -this.width / 2,
      -this.height / 2,
      this.width,
      this.height
    );
    ctx.restore();
  };
  this.move = () => {
    if (!this.onScreen) return false;
    this.posy += this.vely;
    this.checkLife();
  };

  this.checkLife = () => {
    if (this.posy > canvas.height) this.onScreen = false;
    for (var p of paths) {
      if (collisioncheckz(this, p)) {
        this.onScreen = false;
        return false;
      }
    }
    for (var x of houses) {
      if (!x.onScreen) continue;
      if (collisioncheckz(this, x)) {
        this.onScreen = false;
        x.hitHouse();
        if (x.lives < 1) {
          x.onScreen = false;
          simulateDestruction(x, x.colx);
        }
        return false;
      }
    }
    if (collisioncheckz(this, hcs[0])) {
      if (hcs[0].onScreen) {
        hcs[0].start_blinking();
        if (hcs[0].hits < hcs[0].hitlimit) {
          hcs[0].hits += 1;
          hcs[0].lives -= 1;
          this.onScreen = false;
          return false;
        }
        hcs[0].onScreen = false;
        this.onScreen = false;
        // simulateDestruction(hcs[0], "#FF0000");
      }
      return false;
    }
  };
}
