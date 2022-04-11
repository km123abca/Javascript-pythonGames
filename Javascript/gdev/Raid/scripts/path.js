	function path(posx2,posy2,wid,hei)
		{
		this.posx=posx2;
		this.posy=posy2;
		this.width=wid;
                this.height=hei;

                
					
		this.onScreen=true;
                this.hooked=false;

		this.img=new Image();
                this.img.src="sprites/greenstrip.png";

                
                
                this.xpts=[-this.width/2,this.width/2,this.width/2,-this.width/2];
                this.ypts=[-this.height/2,-this.height/2,this.height/2,this.height/2];


	
		
		

		this.dr_w= function()
				{
				if(!this.onScreen) return false;			
				if(mode=='dev')
                                  this.clickAndMove();				
				ctx.save();
                                ctx.fillStyle="#49b9c3";
				ctx.translate(this.posx-camx,this.posy-camy);
                              
				//ctx.rotate(this.rotangle*Math.PI/180);
				ctx.drawImage(this.img,-this.width/2,-this.height/2,this.width,this.height);	
                                ctx.fill();		
				
				ctx.restore();
                                if(this.hcode)
                                 this.dr_w_border();
				};
               this.dr_w_border= function()
				{
				if(!this.onScreen) return false;			

				ctx.save();
				ctx.translate(this.posx-camx,this.posy-camy);	
				
				ctx.strokeStyle='#000000';
				ctx.beginPath();
				ctx.moveTo(this.xpts[0],this.ypts[0]);
				for(var g=1;g<this.xpts.length;g++)
					ctx.lineTo(this.xpts[g],this.ypts[g]);
				ctx.closePath();				
				ctx.stroke();			

				ctx.restore();
				};
               
		this.clickAndMove=()=>
				{
                                if(!mousePress) 
                                   { 
                                   this.hooked=false;
                                   return false;
                                   }
                                if(this.hooked)
                                   {
                                    this.posx=mouseX;
                                    this.posy=mouseY;

				  if(upPress) this.height+=yy;
                                  if(downPress) this.height-=yy;
                                  if(leftPress) this.width-=xx;
                                  if(rightPress) this.width+=xx;
                                  str2print2=((this.posx/xx).toFixed(0)+","+(this.posy/yy).toFixed(0)+","+(this.width/xx).toFixed(0)+","+(this.height/yy).toFixed(0));

                                    return true;
                                   }
				if( (mouseX>(this.posx-this.width/2)) &&
                                    (mouseX<(this.posx+this.width/2)) &&
                                    (mouseY>(this.posy-this.height/2)) &&
                                    (mouseY<(this.posy+this.height/2))
                                  )
				  {
				  this.hooked=true;
				  
                                  return true;
			          }
                                return false;
				};		
			
		
		}