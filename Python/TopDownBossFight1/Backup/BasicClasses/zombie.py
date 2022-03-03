##Zombie starts###
class Zombie:
	def __init__(self,x,y,width,height):
		self.onScreen=True
		self.position=CreateVector(x*xscale,y*yscale)	
		self.width=int(width*xscale)
		self.height=int(height*yscale)
		self.boxCollider=collisionBox(x,y,self.width*0.5,self.height*0.5)
		self.angle=0
		self.idle_images,self.attack_images,self.move_images=[],[],[]
		self.imageLoaders=[['idle','skeleton-idle_',17,self.idle_images],
						   ['move','skeleton-move_',13,self.move_images],
						   ['attack','skeleton-attack_',13,self.attack_images]
						  ]
		for x in self.imageLoaders:
			for i in range(x[2]):
				imagex=pygame.transform.scale(pygame.image.load(f'./sprites/Zombie/{x[0]}/{x[1]+str(i)}.png'),(self.width,self.height))
				x[3].append(imagex)
		self.images=[self.idle_images,self.move_images,self.attack_images]
		self.animTimers=[0,0,0]
		self.animTimersMax=[1,1,2]
		self.anim=0
		self.frame=0
		self.animInQueue=None
		self.velocityMax=10*xscale
		self.enemy=gameManager.player
		self.enemyProxim=60*xscale
		self.hitBoxSpawn=positionBlock(self.position.x,self.position.y,40*xscale,10*yscale,0,0.3*self.width,0.3*self.width)
		self.state="idle"
		self.maxAttackGap=2.5
		self.attackGap=self.maxAttackGap-random.random()
		self.attacks=[]
		self.lastAttackTime=0
		self.maxHealth=100
		self.health=self.maxHealth
		self.healthBar=HealthBar(self.position.x,self.position.y,0,-80*yscale,-40*xscale,200*xscale,10*yscale,self.health,False)
		self.healthBarHidden=False
		self.healthBarClock=0
		self.healthBarMaxTime=2
		self.enemyDirection=CreateVector(0,0)

	def ShowHealthBar(self):
		self.healthBarHidden=False
		self.healthBarClock=time.time()

	def HideHealthBar(self):
		if not self.healthBarHidden:			
			if time.time()-self.healthBarClock > self.healthBarMaxTime:
				self.healthBarHidden=True
	def updateAndDrawHealthBar(self):
		self.HideHealthBar()
		self.healthBar.update(-self.angle,self.position)
		if not self.healthBarHidden:
			self.healthBar.display()

	def update(self):
		self.updateAndDrawHealthBar()
		self.boxCollider.updateP(self.position)
		self.RunStateMachine()
		self.hitBoxSpawn.update(self.angle,self.position)

	def display(self):
		rotated_image=pygame.transform.rotate(self.images[self.anim][self.frame],-self.angle)
		myrect=rotated_image.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y
		win.blit(rotated_image,myrect)
		self.updateAnimation()
		# self.hitBoxSpawn.display()
		# self.boxCollider.display()

	def RunStateMachine(self):
		if self.state=="idle":
			self.DoIdleStuff()

	def DoIdleStuff(self):
		pass

	def updateAnimation(self):
		if not self.clearToAnim():
			return
		self.frame+=1
		if self.frame >= len(self.images[self.anim]):
			if not self.animInQueue:
				self.frame=0
			else:
				self.changeAnimation(self.animInQueue)
				self.animInQueue=None

	def clearToAnim(self):
		self.animTimers[self.anim]+=1
		if self.animTimers[self.anim] >= self.animTimersMax[self.anim]:
			self.animTimers[self.anim]=0
			return True
		return False



##Zombie ends###