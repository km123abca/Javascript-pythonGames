function house(posx2, posy2, wid, hei) {
  this.posx = posx2;
  this.posy = posy2;
  this.width = wid;
  this.height = hei;
  this.img = new Image();
  this.imgs = ["house.png", "housetrans.png", "house.png"];
  this.img.src = `./sprites/${
    this.imgs[Math.floor(this.imgs.length * Math.random())]
  }`;

  this.blinkTimer = 0;
  this.blinkLimiter = 14;
  this.blinking = false;
  this.blinkPeriod = 50;

  this.colx = "#ffff50";

  this.onScreen = true;
  this.hooked = false;
  this.lives = 10;

  this.xpts = [0, this.width, this.width, 0];
  this.ypts = [
    -this.height / 2,
    -this.height / 2,
    this.height / 2,
    this.height / 2,
  ];

  this.letDraw = () => {
    if (!this.blinking) return true;
    this.blinkTimer += 1;
    if (this.blinkTimer >= this.blinkPeriod) {
      this.blinking = false;
      this.blinkTimer = 0;
      return true;
    }
    if (this.blinkTimer % this.blinkLimiter == 0) {
      return false;
    }
    return true;
  };
  this.hitHouse = () => {
    this.blinking = true;
    this.lives -= 1;
    this.updateBlinkLimit();
  };
  this.updateBlinkLimit = () => {
    this.blinkLimiter -= 1;
  };

  this.dr_w = function () {
    if (!this.onScreen) return false;
    if (!this.letDraw()) return false;
    if (mode == "dev") this.clickAndMove();
    ctx.save();
    ctx.translate(this.posx - camx, this.posy - camy);
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
    if (fPress) {
      this.rotangle -= 2;
      if (this.rotangle < 180) this.rotangle += 2;
    }
    if (gPress) {
      this.rotangle += 2;
      if (this.rotangle > 360) this.rotangle -= 2;
    }
  };

  this.clickAndMove = () => {
    if (!mousePress) {
      this.hooked = false;
      return false;
    }
    if (this.hooked) {
      this.posx = mouseX;
      this.posy = mouseY;

      if (upPress) this.height += yy;
      if (downPress) this.height -= yy;
      if (leftPress) this.width -= xx;
      if (rightPress) this.width += xx;
      str2print2 =
        (this.posx / xx).toFixed(0) +
        "," +
        (this.posy / yy).toFixed(0) +
        "," +
        (this.width / xx).toFixed(0) +
        "," +
        (this.height / yy).toFixed(0);

      return true;
    }
    if (
      mouseX > this.posx - this.width / 2 &&
      mouseX < this.posx + this.width / 2 &&
      mouseY > this.posy - this.height / 2 &&
      mouseY < this.posy + this.height / 2
    ) {
      this.hooked = true;

      return true;
    }
    return false;
  };
}
