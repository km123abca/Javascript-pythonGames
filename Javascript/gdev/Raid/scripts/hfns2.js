function raycaster(targetobj, startpt, rayLength, angleRange, scan = false) {
  //startpt => {x:33,y:44}  angleRange=>[90,91]
  var start_angle = 0,
    start_length;
  var end_angle = 0;
  start_angle = angleRange[0];
  end_angle = angleRange[1];

  for (; start_angle < end_angle; start_angle++) {
    start_length = 0;
    var itercontrol = 0;
    while (start_length < rayLength) {
      itercontrol += 1;
      if (itercontrol > 5000) {
        alert("danger");
        break;
      }
      var targy =
        startpt.y + start_length * Math.sin((start_angle / 180) * Math.PI);
      var targx =
        startpt.x + start_length * Math.cos((start_angle / 180) * Math.PI);
      // console.log('search at '+targx+','+targy);
      // console.log(`x:bounds:${targetobj.posx},${targetobj.posx+targetobj.width} `);
      // console.log(`y:bounds:${targetobj.posy},${targetobj.posy+targetobj.height} `);
      if (scan) {
        drawLine(startpt.x, startpt.y, targx, targy);
        // console.log("drawing line");
      }
      if (
        targx > targetobj.posx - targetobj.width / 2 &&
        targx < targetobj.posx + targetobj.width / 2 &&
        targy > targetobj.posy - targetobj.height / 2 &&
        targy < targetobj.posy + targetobj.height / 2
      )
        return [true, start_angle, start_length];
      // console.log('nothing found');
      start_length += 1;
    }
  }
  return [false, 999, 999];
}

function dblClickDetector(tlimit = 20) {
  this.timer = 0;
  this.timerLimit = tlimit;
  this.clickedOnce = false;
  this.trigger = true;
  this.run = () => {
    if (!mousePress) {
      this.trigger = true;

      if (this.timer != 0) {
        this.timer += 1;
        if (this.timer > this.timerLimit) {
          this.timer = 0;
          this.clickedOnce = false;
        }
      }
    }
    if (mousePress && this.trigger) {
      this.trigger = false;
      if (!clickedOnce) {
        this.clickedOnce = true;
        this.timer = 1;
        return false;
      } else {
        this.clickedOnce = false;
        this.timer = 0;
        return true;
      }
    }
    return false;
  };
}

function flushArray(arr) {
  var lis = [];
  for (var i in arr) {
    if (!arr[i].onScreen) lis.push(i);
  }
  for (var i in lis) {
    arr.splice(lis[i], 1);
    for (var j in lis) lis[j] -= 1;
  }
}

function selcol(rb) {
  var rnum = Math.random() * rb.length;
  rnum = Math.floor(rnum);
  rnum = parseInt(rnum);
  return rb[rnum];
}
function cordtrans(x1, y1, ang) {
  var x1new = x1 * Math.cos(d2r(ang)) + y1 * Math.sin(d2r(ang));
  var y1new = -x1 * Math.sin(d2r(ang)) + y1 * Math.cos(d2r(ang));
  return [x1new, y1new];
}
function cordretrans(x1, y1, ang) {
  var x1new = x1 * Math.cos(d2r(ang)) - y1 * Math.sin(d2r(ang));
  var y1new = x1 * Math.sin(d2r(ang)) + y1 * Math.cos(d2r(ang));
  return [x1new, y1new];
}
function cppos(px, py, ang, depth) {
  return true;
}

function d2r(ang) {
  return (ang / 180) * Math.PI;
}
function r2d(ang) {
  return (ang / Math.PI) * 180;
}
function fixinc(angle1, angle2) {
  var a1 = angle1;
  var a2 = angle2;
  if (a1 >= 270) a1 = a1 - 360;
  if (a2 >= 270) a2 = a2 - 360;
  var outputt = ((a2 - a1) / Math.abs(a2 - a1)) * angle_increment;
  return outputt;
}

function getRandomAngle(ang = 90) {
  //console.log('random angle generator called');
  var c_ang = Math.random() * ang;

  if (Math.random() < 0.5) c_ang = 360 - c_ang;
  //console.log('angle:'+c_ang);
  return c_ang;
}

function anglecalc(x1, y1, x2, y2) {
  //console.log('received :'+x1+','+y1+'  and '+x2+','+y2);
  var ygap = y2 - y1;
  var xgap = x2 - x1;
  console.log("ygap:" + ygap);
  console.log("xgap:" + xgap);
  var angindeg = (Math.atan(Math.abs(ygap) / Math.abs(xgap)) * 180) / Math.PI;
  //console.log('angle before processing:'+angindeg);
  if (xgap < 0 && ygap > 0) angindeg = 180 - angindeg;
  if (xgap < 0 && ygap < 0) angindeg = 180 + angindeg;
  if (xgap > 0 && ygap < 0) angindeg = 360 - angindeg;
  console.log("angle after processing:" + angindeg);
  return angindeg;
}
function spawnbarrels() {
  var count = 0;
  for (var i in barrellist) if (barrellist[i].onScreen) count += 1;
  //console.log('THere are '+count+' barrels');
  if (count < 1) barrellist.push(new barrel(25, 25));
}

function keeptimer() {
  t_master += 1;
  if (t_master > 200) {
    alert("Game Over, Score:" + score);
    window.location.href = "f_main.html";
  }
  tt += 1;
  if (tt % 30 == 0) score += 1;
  if (tt > 3000) tt = 0;
}
function markarea(sx, sy) {
  ctx.save();
  ctx.translate(sx, sy);
  //ctx.rotate(this.rotangle*Math.PI/180);
  ctx.fillStyle = "#FF0000";
  ctx.strokeStyle = "#000000";
  ctx.beginPath();
  ctx.arc(0, 0, 10, 0, 2 * Math.PI);
  ctx.stroke();
  ctx.fill();
  ctx.restore();
}

function getcolorrr(hexval) {
  var colis = [
    ["red", "#FF0000"],
    ["green", "#00FF00"],
    ["blue", "#0000FF"],
    ["dark", "#F2F2F2"],
  ];
  var selval = "#FF0000";
  for (var i in colis) {
    if (colis[i][0] == hexval) {
      selval = colis[i][1];
      return selval;
    }
  }
  return selval;
}

function dispscore(idd, strr) {
  document.getElementById(idd).value = strr;
}
function calcDist(x1, y1, x2, y2) {
  var xsep = Math.abs(x1 - x2);
  var ysep = Math.abs(y1 - y2);
  var dist = Math.sqrt(xsep * xsep + ysep * ysep);
  return dist;
}

function collisioncheckz(elem1, elem2) {
  return inter_ects(
    elem1.posx - elem1.width / 2,
    elem1.posy - elem1.height / 2,
    elem1.width,
    elem1.height,
    elem2.posx - elem2.width / 2,
    elem2.posy - elem2.height / 2,
    elem2.width,
    elem2.height
  );
}

function cza(elem1, elem2, ang) {
  var x1dupe = elem1.posx - elem1.width / 2;
  var y1dupe = elem1.posy - elem1.height / 2;
  var x2dupe = elem2.posx - elem2.width / 2;
  var y2dupe = elem2.posy - elem2.height / 2;

  var x1 =
    x1dupe * Math.cos((Math.PI / 180) * ang) +
    y1dupe * Math.sin((Math.PI / 180) * ang);
  var y1 =
    y1dupe * Math.cos((Math.PI / 180) * ang) -
    x1dupe * Math.sin((Math.PI / 180) * ang);
  var x2 =
    x2dupe * Math.cos((Math.PI / 180) * ang) +
    y2dupe * Math.sin((Math.PI / 180) * ang);
  var y2 =
    y2dupe * Math.cos((Math.PI / 180) * ang) -
    x2dupe * Math.sin((Math.PI / 180) * ang);
  return inter_ects(
    x1,
    y1,
    elem1.width,
    elem1.height,
    x2,
    y2,
    elem2.width,
    elem2.height
  );
}

function inter_ects(q1, q2, ql1, ql2, w1, w2, wl1, wl2) {
  if (w1 >= q1) {
    if (w1 - q1 < ql1) {
      if (w2 >= q2) {
        if (w2 - q2 < ql2) return true;
        return false;
      } else {
        if (q2 - w2 < wl2) return true;
        return false;
      }
    }
  } else {
    if (q1 - w1 < wl1) {
      if (w2 >= q2) {
        if (w2 - q2 < ql2) return true;
        return false;
      } else {
        if (q2 - w2 < wl2) return true;
        return false;
      }
    }
  }
}

function outAbounds(px, py) {
  if (!(px >= 0 && px <= canvas.width && py >= 0 && py <= canvas.height))
    return true;
  return false;
}
