    
    function r2d(angle) 
        {
            return angle/Math.PI * 180;
        }
    function d2r(angle)
        {
            return angle/180*Math.PI;
        }
    function createVector(x,y)
        {
            this.x=x;
            this.y=y;
            this.copy=()=>
                {
                    let newVec=new createVector(this.x,this.y);
                    return newVec;
                }
            this.set=(x,y)=>
                {
                    this.x=x;
                    this.y=y;
                }
            this.add=(x)=>
                {
                    this.x+=x.x;
                    this.y+=y.y;
                }
            this.sub=(x)=>
                {
                    this.x-=x.x;
                    this.y-=x.y;
                }
            this.mult=(x)=>
                {
                    this.x*=x;
                    this.y*=x;
                }
            this.normalize=()=>
                {
                    let mag=Math.sqrt(this.x**2+this.y**2);
                    this.x=this.x/mag;
                    this.y=this.y/mag;
                }
            this.mag=()=>
                {
                    return Math.sqrt(this.x**2+this.y**2);
                }
            this.heading=()=>
                {
                    let ang=Math.atan2(this.y,this.x)/Math.PI*180;
                    if(ang < 0) ang+=360;
                    return ang;
                }
        }
    function flushArray(arr) 
        {
        var lis = [];
        for (var i in arr) 
            {
            if (!arr[i].onScreen) lis.push(i);
            }
      for (var i in lis) 
            {
            arr.splice(lis[i], 1);
            for (var j in lis) lis[j] -= 1;
            }
        }
    let DistBween=(x1,y1,x2,y2)=>
                                {
                                    return Math.sqrt((x1-x2)**2+(y1-y2)**2);
                                };
    let Lerp=(startValue,endValue,lerpFac=2)=>
    								{
    									return startValue+(endValue-startValue)/lerpFac;
    								};
	function collisioncheckz(elem1,elem2)
				{
			return (inter_ects(elem1.posx-elem1.width/2,elem1.posy-elem1.height/2,
							   elem1.width,elem1.height,
					   		   elem2.posx-elem2.width/2,elem2.posy-elem2.height/2,
					   		   elem2.width,elem2.height
					  		  )
				   );
				}
	function inter_ects(q1,q2,ql1,ql2,w1,w2,wl1,wl2)
				{
				if(w1>=q1)
					{
					if((w1-q1)<ql1)
						{
						if(w2>=q2)
							{
							if((w2-q2)<ql2) return true;
							return false;
							}
						else
							{
							if((q2-w2)<wl2) return true;
							return false;
							}
						}
					}
				else
					{
					if((q1-w1)<wl1)
						{
						if(w2>=q2)
							{
							if((w2-q2)<ql2) return true;
							return false;
							}
						else
							{
							if((q2-w2)<wl2) return true;
							return false;
							}
						}
					}
				}

    