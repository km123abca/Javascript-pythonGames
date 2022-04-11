function destro(posx2, posy2, color) {
  this.posx = posx2;
  this.posy = posy2;
  this.height = smallblocksize;
  this.width = smallblocksize;
  this.color = color;
  this.onScreen = true;
  this.xpts = [
    -this.width / 2,
    -this.width / 2,
    this.width / 2,
    this.width / 2,
  ];
  this.ypts = [
    this.height / 2,
    -this.height / 2,
    -this.height / 2,
    this.height / 2,
  ];
  this.velx = Math.random() * 5 - 2.5;
  this.vely = 2 + Math.random() * 5;
  this.img = new Image();
  this.lifeStartTime=0;

  this.img.src = "./sprites/cloud.png";
  this.mindLife=()=>{
    this.lifeStartTime+=1;
    if(this.lifeStartTime > 120)
      this.onScreen=false;

  };
  this.dr_w = function () {
    if (!this.onScreen) return false;
    ctx.save();
    ctx.translate(this.posx - camx, this.posy - camy);
    ctx.fillStyle = this.color;
    ctx.drawImage(
      this.img,
      -this.width / 2,
      -this.height / 2,
      this.width,
      this.height
    );
    ctx.fill();
    ctx.restore();
  };

  this.dr_w_old = function () {
    if (!this.onScreen) return false;
    ctx.save();
    ctx.translate(this.posx, this.posy);
    ctx.fillStyle = this.color;
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
  this.move = function () {
    if (!this.onScreen) return false;
    this.mindLife();
    this.posx += this.velx;
    this.posy += this.vely;
    this.checkwalls();
  };
  this.checkwalls = function () {
    if (this.posx - camx > canvas.width || this.posx - camx < 0)
      this.onScreen = false;
    if (this.posy - camy > canvas.height || this.posy - camy < 0)
      this.onScreen = false;
  };
}
