function cannonArm(posx2, posy2, wid, hei, master) {
  this.posx = posx2;
  this.posy = posy2;
  this.width = wid;
  this.height = hei;
  this.rotangle = 180;

  this.onScreen = true;
  this.hooked = false;
  this.img = new Image();
  this.img.src = "./sprites/cannonarm.png";
  this.rotVel = 2;

  this.locked = false;
  this.locked_lost = false;
  this.target_id = -1;
  this.accelerating = true;
  this.latchVelAcc = 0.5;
  this.latchVel = 2;
  this.master = master;
  this.lockedTarget = "";
  this.highEnd = 360;
  this.lowEnd = 180;

  this.xpts = [0, this.width, this.width, 0];
  this.ypts = [
    -this.height / 2,
    -this.height / 2,
    this.height / 2,
    this.height / 2,
  ];

  this.dr_w = function () {
    if (!this.onScreen) return false;

    ctx.save();
    ctx.translate(this.posx, this.posy);
    ctx.rotate((this.rotangle * Math.PI) / 180);
    //     ctx.fillStyle = "#00FFFF";
    //     ctx.strokeStyle = "#000000";
    //     ctx.beginPath();
    //     ctx.moveTo(this.xpts[0], this.ypts[0]);
    //     for (var g = 1; g < this.xpts.length; g++)
    //       ctx.lineTo(this.xpts[g], this.ypts[g]);
    //     ctx.closePath();
    //     ctx.stroke();
    //     ctx.fill();
    ctx.drawImage(this.img, 0, -this.height / 2, this.width, this.height);

    ctx.restore();
  };
  this.move = () => {
    if (!this.onScreen) return false;
    if (!this.locked) {
      if (Math.abs(this.rotVel) != 2) {
        this.highEnd = 360;
        this.lowEnd = 180;
        this.rotVel = 2;
      }
      this.latchOn();
    } else {
      // this.maintainLock();
      this.maintainLockAbsolute();
    }
    this.rotangle += this.rotVel;
    if (this.rotangle > this.highEnd) {
      this.rotangle -= this.rotVel;
      this.rotVel *= -1;
    }
    if (this.rotangle < this.lowEnd) {
      this.rotangle -= this.rotVel;
      this.rotVel *= -1;
    }

    /*
    if (fPress) {
      this.rotangle -= 2;
      if (this.rotangle < 180) this.rotangle += 2;
    }
    if (gPress) {
      this.rotangle += 2;
      if (this.rotangle > 360) this.rotangle -= 2;
    }
    */
  };
  this.maintainLockAbsolute = () => {
    if (this.lockedTarget == "") return false;
    if (!this.lockedTarget.onScreen || !this.lockedTarget.isVisible) {
      this.locked = false;
      this.target_id = -1;
      this.lockedTarget = "";
      return false;
    }
    let xdiff = this.lockedTarget.posx - this.master.posx;
    let ydiff = this.lockedTarget.posy - this.master.posy;
    let angle = r2d(Math.atan(Math.abs(ydiff) / Math.abs(xdiff)));
    if (xdiff < 0) angle = 180 + angle;
    else angle = 360 - angle;

    /*
    this.highEnd = angle + 5;
    this.lowEnd = angle - 5;
    this.rotVel = 0.25;
    if (this.rotangle > this.highEnd || this.rotangle < this.lowEnd)
      this.rotangle = angle;
    */
    this.rotVel = 0;
    this.rotangle = angle;
  };

  this.maintainLock = () => {
    this.decideRotation();
    this.rotangle += this.latchVel;
    if (this.rotangle > 360 || this.rotangle < 180)
      this.rotangle -= this.latchVel;

    if (!this.latchStillOn()) {
      // this.locked_lost=true;
      if (!this.accelerating) {
        this.latchVel =
          (Math.abs(this.latchVel) + this.latchVelAcc) *
          (this.latchVel / Math.abs(this.latchVel));
        // this.accelerating = true;
      } else {
        this.latchVel =
          (Math.abs(this.latchVel) - this.latchVelAcc) *
          (this.latchVel / Math.abs(this.latchVel));
        // this.accelerating = false;
      }
    }
  };
  this.latchStillOn = () => {
    let planeFound = false;
    for (var plane of hostiles) {
      if (!plane.onScreen) continue;
      if (plane.plane_id == this.target_id) {
        planeFound = true;
        [onRadar] = raycaster(
          plane,
          { x: this.master.posx, y: this.master.posy },
          canvas.height,
          [this.rotangle, this.rotangle + 1],
          false
        );
        if (onRadar) return true;
      }
    }
    if (!planeFound) {
      console.log("latch lost");
      this.locked = false;
      this.target_id = -1;
      this.latchVel = this.rotVel;
      this.lockedTarget = "";
      this.accelerating = false;
    }
    return false;
  };
  this.latchOn = () => {
    if (this.locked) return false;
    for (var plane of hostiles) {
      if (!plane.onScreen) continue;
      // console.log(canvas.height + "," + this.rotangle);
      [onRadar] = raycaster(
        plane,
        { x: this.master.posx, y: this.master.posy },
        canvas.height,
        [this.rotangle, this.rotangle + 1],
        false
      );
      if (onRadar) {
        this.locked = true;
        this.target_id = plane.plane_id;
        this.lockedTarget = plane;
        // this.decideRotation();

        return true;
      }
    }
  };

  this.decideRotation = () => {
    if (this.lockedTarget.velx > 0) {
      this.latchVel = Math.abs(this.latchVel);
    } else if (this.lockedTarget.velx == 0) this.latchVel = 0;
    else this.latchVel = -Math.abs(this.latchVel);
  };
}
