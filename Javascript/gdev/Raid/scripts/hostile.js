function hostile(posx2, posy2, velx = -1 * xx, testh = false) {
  this.posx = posx2;
  this.posy = posy2;
  this.width = 140;
  this.height = 67;
  this.testh = testh;
  this.plane_id = getId();
  this.isVisible = false;
  this.resil = 0;
  this.startDestruction = false;
  this.deathTimer = 0;
  this.deathLimit = 100;
  this.rotangle = 0;

  this.sx = 1;
  this.sy = 1;
  if (velx < 0) this.sx = -1;

  this.onScreen = true;
  this.velx = velx;
  this.vely = 0;
  // if (this.testh) this.velx = 0;
  this.xpts = [-60, -41, 57, 80, 75, -28];
  this.ypts = [-2, -22, -24, -49, 17, 18];

  this.in_screen = false;
  this.hits = 0;

  this.fire_timer = 0;
  this.fire_limit = 20;
  this.img = new Image();
  this.img.src = "./sprites/fplane.png";
  this.fire = () => {
    this.fire_timer += 1;
    if (this.fire_timer < this.fire_limit) return false;
    this.fire_timer = 0;
    if (Math.random() < 0.5) bombs.push(new bomb(this.posx, this.posy));
  };

  this.adjustRotation = () => {
    if (this.velx < 0) this.rotangle = 355;
    else this.rotangle = 5;
  };
  this.destroySelf = () => {
    this.startDestruction = true;
    this.vely = 1 * yy;
    this.adjustRotation();
  };
  this.initiateExplosion = () => {
    if (!this.startDestruction) return false;
    this.deathTimer += 1;
    if (this.deathTimer > this.deathLimit) {
      this.onScreen = false;
      simulateDestruction(this, "#FFFF00");
    }
  };

  this.dr_w = function () {
    if (!this.onScreen) return false;
    this.initiateExplosion();
    ctx.save();
    ctx.translate(this.posx - camx, this.posy - camy);
    ctx.rotate((this.rotangle * Math.PI) / 180);
    ctx.scale(this.sx, this.sy);
    //     ctx.fillStyle = "#FF00FF";
    //     ctx.strokeStyle = "#000000";
    //     ctx.beginPath();
    //     ctx.moveTo(this.xpts[0], this.ypts[0]);
    //     for (var g = 1; g < this.xpts.length; g++)
    //       ctx.lineTo(this.xpts[g], this.ypts[g]);
    //     ctx.closePath();
    //     ctx.stroke();
    //     ctx.fill();
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
    this.is_inscreen();
    this.checkVisibility();
    if (this.testh) this.manualMove();
    else {
      this.fire();
      this.posx += this.velx;
      this.posy += this.vely;
    }
    this.wallCheck();
  };

  this.manualMove = () => {
    // this.posx -= this.velx;

    if (fPress) this.velx = 2;
    else if (gPress) {
      // console.log("gvelx is " + this.velx);
      this.velx = -2;
    } else {
      // console.log("velx is " + this.velx);
      this.velx = 0;
    }
    // console.log(this.velx);
    this.posx += this.velx;
  };

  this.is_inscreen = () => {
    if (this.in_screen) return true;
    if (
      this.posx - camx + this.width / 2 < canvas.width &&
      this.posx - camx - this.width / 2 > 0 &&
      this.posy - camy < canvas.height &&
      this.posy - camy > 0
    )
      this.in_screen = true;
  };

  this.checkVisibility = () => {
    this.isVisible = false;
    if (this.posx - camx > 0 && this.posx - camx < canvas.width)
      this.isVisible = true;
  };
  this.wallCheck = () => {
    if (!this.in_screen) return false;

    if (this.posx - camx - this.width / 2 > 2 * canvas.width)
      this.posx = camx - 200;
    if (this.posx - camx + this.width / 2 < 0)
      this.posx = camx + canvas.width + 200;
  };
}
