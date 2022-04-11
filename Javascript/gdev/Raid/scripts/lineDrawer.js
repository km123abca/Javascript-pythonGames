	function lineDrawer(posx,posy)
		{
		

                this.posx=posx;
                this.posy=posy;
					
		this.onScreen=true;
                
                this.mouseTrigger=true;
                this.delTrigger=true;
		
                //this.pts=[[-10*xx,-10*yy],[20*xx,20*yy]];
                this.pts=[];
             
             this.delPts=()=>{
                              if(!upPress) this.delTrigger=true;
                              if(upPress && this.delTrigger)
                                  {
                                     this.delTrigger=false;
                                     this.pts.pop();
                                  }
                             }
                
              this.addPointOnClick=()=>{
                                         if(!mousePress) 
                                           this.mouseTrigger=true;

                                         if(mousePress && this.mouseTrigger)
                                           {
                                             this.mouseTrigger=false;
                                             this.pts.push([mouseX-this.posx,mouseY-this.posy]);
                              
                                           }
                                       };
                
              this.displayCoords=()=>{
               w2screen("center:"+(this.posx/xx).toFixed(0)+","+(this.posy/yy).toFixed(0),20*xx,80*yy);
               for(var i in this.pts)
                    {
                      elem=this.pts[i];
                      w2screen("x:"+(elem[0]/xx).toFixed(0)+",y:"+(elem[1]/yy).toFixed(0),20*xx,100*yy+i*20*yy);
                    }

              };
		
		

		
               this.dr_w= function()
				{
				if(!this.onScreen) return false;			

				ctx.save();
				ctx.translate(this.posx-camx,this.posy-camy);	
				 
                                ctx.fillStyle='#00FFFF';
				ctx.strokeStyle='#00FF00';
				ctx.beginPath();
                                if(this.pts.length>0)
				ctx.moveTo(this.pts[0][0],this.pts[0][1]);
				for(var g=1;g<this.pts.length;g++)
					ctx.lineTo(this.pts[g][0],this.pts[g][1]);
				ctx.closePath();				
				ctx.stroke();
                                //ctx.fill();			

				ctx.restore();
                                this.displayCoords();
                                this.addPointOnClick();
                                this.dr_w_pt();
                                this.delPts();
				};      
		this.dr_w_pt= function()
				{
				if(!this.onScreen) return false;
				
								
				ctx.save();
				ctx.translate(this.posx,this.posy);
				
				ctx.fillStyle='#2d4f83';
				ctx.strokeStyle='#000000';
				ctx.beginPath();
				ctx.arc(0,0,10*xx,0,2*Math.PI);
				ctx.stroke();
				ctx.fill();
				
				
				ctx.restore();
				};
                this.shift=()=>
                               {
                                this.posx=mouseX;
                                this.posy=mouseY;
                                this.pts.pop();
                                this.pts.pop(); 
                               }
		
		}