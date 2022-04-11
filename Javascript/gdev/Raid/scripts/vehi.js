function vehi(posx2, posy2, wid, hei) {
  this.posx = posx2;
  this.posy = posy2;
  this.width = wid;
  this.height = hei;
  this.colx = "#00bcbe";

  this.onScreen = true;
  this.hooked = false;

  this.velx = 5 * xx;
  this.hits = 0;
  this.hitlimit = 20;
  this.lives = 20;

  this.img = new Image();
  this.img.src = "./sprites/tank_alone.png";

  this.arm = new cannonArm(0, 0, 0.8 * this.width, 0.4 * this.height, this);

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

  this.fire_timer = 0;
  this.fire_limit = 5;

  this.blinking = true;
  this.blinking_timer = 0;
  this.blinking_limit = 100;
  this.showTimer = 0;
  this.showLimit = 3;

  this.start_blinking = () => {
    if (this.blinking) return false;
    this.blinking = true;
  };
  this.maintainBlink = () => {
    if (!this.blinking) return true;

    this.blinking_timer += 1;
    if (this.blinking_timer > this.blinking_limit) {
      this.blinking_timer = 0;
      this.blinking = false;
    }
    return this.showImage();
  };
  this.showImage = () => {
    if (!this.blinking) return true;
    this.showTimer += 1;
    if (this.showTimer > this.showLimit) {
      this.showTimer = 0;
      return true;
    }
    return false;
  };

  this.showLife = () => {
    str2print2 = "score:" + this.lives;
  };

  this.fire = () => {
    this.fire_timer += 1;
    if (this.fire_timer < this.fire_limit) return false;
    this.fire_timer = 0;
    var tip = { x: "", y: "" };
    tip.x =
      this.posx +
      this.arm.width * Math.cos((this.arm.rotangle / 180) * Math.PI);
    tip.y =
      this.posy +
      this.arm.width * Math.sin((this.arm.rotangle / 180) * Math.PI);

    bullets.push(new bullet(tip.x, tip.y, 10, 10, this.arm.rotangle));
  };

  this.dr_w = function () {
    if (!this.onScreen) return false;
    this.showLife();
    if (mode == "dev") this.clickAndMove();

    ctx.save();
    ctx.translate(this.posx - camx, this.posy - camy);
    if (this.maintainBlink()) {
      this.arm.dr_w();
      ctx.drawImage(
        this.img,
        -this.width / 2,
        -this.height / 2,
        this.width,
        this.height
      );
    }

    ctx.restore();
  };
  this.move = () => {
    if (!this.onScreen) return false;
    if (leftPress) {
      console.log("left is pressed");
      this.posx -= this.velx;
    }
    if (rightPress) {
      this.posx += this.velx;
    }
    this.arm.move();
    this.panCamera();
    if (enterPress) this.fire();
  };

  this.panCamera = () => {
    if (this.posx > 0.8 * canvas.width) moveCamera(0.8 * canvas.width);
    if (this.posx < 0.8 * canvas.width) moveCamera(0);
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
      mouseX > this.posx - this.width / 2 - camx &&
      mouseX < this.posx + this.width / 2 - camx &&
      mouseY > this.posy - this.height / 2 - camy &&
      mouseY < this.posy + this.height / 2 - camy
    ) {
      this.hooked = true;

      return true;
    }
    return false;
  };
}
