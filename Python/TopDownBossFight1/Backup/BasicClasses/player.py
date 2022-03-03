###########################Player Starts########################################
class Player:
	def __init__(self,x,y,wid,hei):
		self.onScreen=True
		
		self.width=int(wid*xscale)
		self.height=int(hei*yscale)
		self.position=CreateVector(x*xscale,y*yscale)
		self.boxCollider=collisionBox(x*xscale,y*yscale,self.width*0.5,self.height*0.5)
		self.shootPosition=positionBlock(x*xscale,y*yscale,45*xscale,25*yscale,0,self.width*0.05,self.height*0.05) #45 25
		

		# self.width=wid
		# self.height=hei
		# self.position=CreateVector(x,y)
		# self.boxCollider=collisionBox(x,y,self.width*0.5,self.height*0.5)
		# self.shootPosition=positionBlock(x,y,45*xscale,25*yscale,0,self.width*0.05,self.height*0.05)

		self.idle_images,self.move_images,self.shoot_images,self.reload_images,self.melee_images=[],[],[],[],[]		
		self.images=[]	
		self.angle=0
		self.animInQueue=None
		self.weaponIndex=0
		self.health=100
		self.maxHealth=100
		self.meleeRegistered=False
		self.healthBar=HealthBar(x,y,0,-80*yscale,-40*xscale,200*xscale,10*yscale,self.maxHealth,False)
		for i in range(19):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/idle/survivor-idle_handgun_{i}.png')),(self.width,self.height))
			self.idle_images.append(imagex)
		for i in range(19):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/move/survivor-move_handgun_{i}.png')),(self.width,self.height))
			self.move_images.append(imagex)
		for i in range(3):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/shoot/survivor-shoot_handgun_{i}.png')),(self.width,self.height))
			self.shoot_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/reload/survivor-reload_handgun_{i}.png')),(self.width,self.height))
			self.reload_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/meleeattack/survivor-meleeattack_handgun_{i}.png')),(self.width,self.height))
			self.melee_images.append(imagex)
		
		#flashlight images
		self.flashlight_idle_images,self.flashlight_melee_images,self.flashlight_move_images=[],[],[]
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'flashlight/idle/survivor-idle_flashlight_{i}.png')),(self.width,self.height))
			self.flashlight_idle_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'flashlight/meleeattack/survivor-meleeattack_flashlight_{i}.png')),(self.width,self.height))
			self.flashlight_melee_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'flashlight/move/survivor-move_flashlight_{i}.png')),(self.width,self.height))
			self.flashlight_move_images.append(imagex)

		#knife images
		self.knife_idle_images,self.knife_melee_images,self.knife_move_images=[],[],[]
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'knife/idle/survivor-idle_knife_{i}.png')),(self.width,self.height))
			self.knife_idle_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'knife/meleeattack/survivor-meleeattack_knife_{i}.png')),(self.width,self.height))
			self.knife_melee_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'knife/move/survivor-move_knife_{i}.png')),(self.width,self.height))
			self.knife_move_images.append(imagex)

		#rifle images
		self.rifle_idle_images,self.rifle_melee_images,self.rifle_move_images,self.rifle_reload_images,self.rifle_shoot_images=[],[],[],[],[]
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/idle/survivor-idle_rifle_{i}.png')),(self.width,self.height))
			self.rifle_idle_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/meleeattack/survivor-meleeattack_rifle_{i}.png')),(self.width,self.height))
			self.rifle_melee_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/move/survivor-move_rifle_{i}.png')),(self.width,self.height))
			self.rifle_move_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/reload/survivor-reload_rifle_{i}.png')),(self.width,self.height))
			self.rifle_reload_images.append(imagex)
		for i in range(3):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/shoot/survivor-shoot_rifle_{i}.png')),(self.width,self.height))
			self.rifle_shoot_images.append(imagex)

		#shotgun images
		self.shotgun_idle_images,self.shotgun_melee_images,self.shotgun_move_images,self.shotgun_reload_images,self.shotgun_shoot_images=[],[],[],[],[]
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/idle/survivor-idle_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_idle_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/meleeattack/survivor-meleeattack_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_melee_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/move/survivor-move_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_move_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/reload/survivor-reload_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_reload_images.append(imagex)
		for i in range(3):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/shoot/survivor-shoot_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_shoot_images.append(imagex)

		self.weaponAnims=[[self.idle_images,self.move_images,self.shoot_images,self.reload_images,self.melee_images],
						  [self.flashlight_idle_images,self.flashlight_move_images,self.flashlight_melee_images,self.flashlight_melee_images,
						   self.flashlight_melee_images],
						  [self.knife_idle_images,self.knife_move_images,self.knife_melee_images,self.knife_melee_images,
						   self.knife_melee_images],
						  [self.rifle_idle_images,self.rifle_move_images,self.rifle_shoot_images,self.rifle_reload_images,
						   self.rifle_melee_images],
						  [self.shotgun_idle_images,self.shotgun_move_images,self.shotgun_shoot_images,self.shotgun_reload_images,
						   self.shotgun_melee_images],
		                  ]


		self.images=[self.idle_images,self.move_images,self.shoot_images,self.reload_images,self.melee_images]
		self.animTimers=[0,0,0,0,0]
		self.animTimerMax=[1,1,1,1,1]
		self.anim=0
		self.frame=0
		
		self.rotationSpeedMin=2		
		self.rotationSpeedAcc=0.25
		self.rotationSpeedMax=20
		self.rotationSpeed=self.rotationSpeedMax

		self.vmax=10*xscale
		self.vmaxOrig=10*xscale
		self.velMin=1
		self.velocity=CreateVector(self.velMin,0)	
		self.vel=self.velMin
		self.bullets=[]
		self.lastShootTime=0
		self.shootGap=0.8	
		self.weaponChangeAuthorized=True

		self.InvincibleMode=False
		self.invincibleStartTime=0
		self.invincibleMaxGap=2
		self.flickerCounter=0

		self.healthBarHidden=False
		self.healthBarClock=0
		self.healthBarMaxTime=3

		self.staggerDir=None
		self.staggerVel=16
		self.stoppedMovement=False
		self.staggering=False
		self.staggerStartTime=0
		self.maxStaggerTime=0.25
		self.reloadCommandGiven=False
		self.dashOn=False
		self.dashStartTime=0
		self.maxDashTime=0.1
		self.dashVelocity=40*xscale
		self.dashTriggerOn=True
		self.maxDashGap=2

		self.lastRifleShot=0
		self.rifleShotGap=0.25
		self.shootCount=0
		self.maxShootCount=3
		self.autoShootOn=False
		self.rifleShots=2
		self.shotGunShots=3

		self.lastBlockTime=0
		self.minGapBetweenBlocks=0

		self.gunStartTime=0
		self.gunMaxTime=4

	def WaitForReloadTime(self):
		if time.time()-self.gunStartTime > self.gunMaxTime:
			self.rifleShots=5
			self.shotGunShots=5

	def MindDash(self):
		if not self.dashOn:
			return
		if time.time()-self.dashStartTime > self.maxDashTime:
			self.dashOn=False
			self.dashStartTime=time.time()

	def ShowHealthBar(self):
		self.healthBarHidden=False
		self.healthBarClock=time.time()
	def HideHealthBar(self):
		if not self.healthBarHidden:			
			if time.time()-self.healthBarClock > self.healthBarMaxTime:
				self.healthBarHidden=True
	def IncreaseRotationSpeed(self):
		if self.rotationSpeed < self.rotationSpeedMax:
			self.rotationSpeed+=self.rotationSpeedAcc

	def ManageInvincibility(self):
		if not self.InvincibleMode:
			return
		if time.time()-self.invincibleStartTime > self.invincibleMaxGap:
			self.InvincibleMode=False
	def TakeDamage(self,dmg,enemyVel=None):	
		if self.InvincibleMode:
			return False	
		self.health-=dmg
		lossBuzz.play()
		self.healthBar.reduceHealth(dmg)
		self.ShowHealthBar()
		if enemyVel:
			self.startStagger(enemyVel)
		self.InvincibleMode=True
		self.invincibleStartTime=time.time()
		if self.health < 0:
			self.health=0
			self.onScreen=False			
			gameManager.SetText("You Died .....")
			SpawnCloudGroup(self.position)
			gameManager.reloadLevel()
			glassBreak.play()
	def changeWeapon(self):
		self.weaponIndex+=1
		if self.weaponIndex >= len(self.weaponAnims):
			self.weaponIndex=0
		self.images=self.weaponAnims[self.weaponIndex]
	def changeWeapons(self):
		if TPRESSED:
			if self.weaponChangeAuthorized:
				self.weaponChangeAuthorized=False
				self.changeWeapon()
				changeBullet(self.presentWeapon())
		elif not self.weaponChangeAuthorized:
			self.weaponChangeAuthorized=True

	def CheckPostPassed(self):
		if self.presentWeapon()=="rifle" and self.rifleShots<=0:
			self.WaitForReloadTime()
			return False
		if self.presentWeapon()=="shotgun" and self.shotGunShots<=0:
			self.WaitForReloadTime()
			return False
		return True

	def shoot(self):
		if self.runningAnimation() in ["shoot","reload","melee"]:
			return False
		if not self.CheckPostPassed():
			#play a sound here
			return
		if time.time()-self.lastShootTime > self.shootGap:
			self.animInQueue=self.runningAnimation()
			if self.presentWeapon() not in ['flashlight','knife','rifle','shotgun']:
				self.bullets.append(bullet(self.shootPosition.position.x,self.shootPosition.position.y,self.angle,self,'player'))
				# print("changed animation to shoot")
				self.ChangeAnimation("shoot")				
				shootingSound.play()
			elif self.presentWeapon()=='shotgun':
				self.shotGunShots-=1
				if self.shotGunShots <= 0:
					self.gunStartTime=time.time()
					# gameManager.PlayerRequest('shotgun')
				self.bullets.append(bullet(self.shootPosition.position.x,self.shootPosition.position.y,self.angle,self,'player'))
				self.ChangeAnimation("shoot")
				parry.play()
			elif self.presentWeapon()=='rifle':
				self.rifleShots-=1
				if self.rifleShots <= 0:
					self.gunStartTime=time.time()
					# gameManager.PlayerRequest("rifle")
				self.autoShootOn=True				
				self.ChangeAnimation("shoot")
			else:				
				self.ChangeAnimation("melee")
			self.lastShootTime=time.time()



	def autoShoot(self):
		if not self.autoShootOn:
			return
		if time.time()-self.lastRifleShot > self.rifleShotGap:
			self.lastRifleShot=time.time()
			self.bullets.append(bullet(self.shootPosition.position.x,self.shootPosition.position.y,self.angle,self,'player'))
			self.shootCount+=1
			shootingSound.play()
			if self.shootCount > self.maxShootCount:
				self.shootCount=0
				self.autoShootOn=False 

	def animUpdateAllowed(self):
		self.animTimers[self.anim]+=1
		if self.animTimers[self.anim] >= self.animTimerMax[self.anim]:
			self.animTimers[self.anim]=0
			return True
		return False

	def FlickerManagerCleared(self):
		if not self.InvincibleMode:
			return True
		self.flickerCounter+=1
		if self.flickerCounter > 100:
			self.flickerCounter=0
		if self.flickerCounter % 3 == 0:
			return True
		return False

	def updateAnimation(self):
		if not self.animUpdateAllowed():
			return False
		
		self.frame+=1		
		if self.frame >= len(self.images[self.anim]):
			if not self.animInQueue:
				self.frame=0
			elif self.runningAnimation()=='shoot':
				self.ChangeAnimation('reload')
			else:
				self.ChangeAnimation(self.animInQueue)
				self.animInQueue=None

	def ChangeAnimation(self,animName):
		if animName=='idle' and self.anim!=0:
			self.anim=0
			self.frame=0
		elif animName=='move' and self.anim!=1:
			self.anim=1
			self.frame=0
		elif animName=="shoot" and self.anim!=2:			
			self.anim=2
			self.frame=0
		elif animName=="reload" and self.anim!=3:			
			self.anim=3
			self.frame=0
		elif animName=="melee" and self.anim!=4:
			self.anim=4
			self.frame=0

	def presentWeapon(self):
		if self.weaponIndex==0:
			return 'handgun'
		elif self.weaponIndex==1:
			return 'flashlight'
		elif self.weaponIndex==2:
			return 'knife'
		elif self.weaponIndex==3:
			return 'rifle'
		elif self.weaponIndex==4:
			return 'shotgun'

	def runningAnimation(self):
		if self.anim==0:
			return 'idle'
		elif self.anim==1:
			return 'move'
		elif self.anim==2:
			return 'shoot'
		elif self.anim==3:
			return 'reload'
		elif self.anim==4:
			return 'melee'


	def updateRunBullets(self,win):
		for x in self.bullets:
			if not x.onScreen:
				continue
			x.display(win)
			x.update()
		flushList(self.bullets)
		############Stagger starts################
	def staggerBack(self):
		if not self.stoppedMovement:
			self.position.add(self.staggerDir.copy().mult(self.staggerVel))
			for elem in gameManager.roadBlocksList:
				if not elem.onScreen:
					continue				
				if boxCollision(self,elem):					
					self.position.add(self.staggerDir.copy().mult(self.staggerVel*-1))
					self.stoppedMovement=True
		if time.time()-self.staggerStartTime > self.maxStaggerTime:
			self.staggering=False
			self.stoppedMovement=False
			self.staggerStartTime=time.time()
	def startStagger(self,enemyVel):		
		self.staggerDir=enemyVel.normalized()
		self.staggering=True
		self.staggerStartTime=time.time()
		############Stagger ends##################

	def HitOnMelee(self):
		if self.presentWeapon()!="knife" and not self.meleeRegistered:
			return
		if self.presentWeapon()=="knife" and self.runningAnimation()=="melee" and self.frame==9 and not self.meleeRegistered:
			# SpawnCloudGroup(self.shootPosition.position)
			for x in gameManager.rocks:
				if not x.onScreen:
					continue
				if boxCollision(self.shootPosition,x):
					SpawnCloudGroup(self.shootPosition.position)
					rockSmash.play()
					x.onScreen=False
			self.meleeRegistered=True
		elif self.runningAnimation()!="melee" and self.meleeRegistered:
			self.meleeRegistered=False

	def BlockWithGun(self):
		if self.InvincibleMode:
			return False
		if time.time()-self.lastBlockTime < self.minGapBetweenBlocks:
			return False
		if self.presentWeapon() in ['knife','flashlight'] or self.runningAnimation() in ['shoot','reload','melee']:
			return False
		self.animInQueue=self.runningAnimation()
		self.ChangeAnimation("melee")
		self.lastBlockTime=time.time()

	def IsBlocking(self):
		if self.runningAnimation()=='melee' and self.frame >3 and self.frame < 13:
			return True
		return False 

	def adjustToDestinationAngle(self,ang):	
		if self.angle==ang:
			self.ApplyVelocity()
			return
		if self.vel > self.velMin:
			self.vel=self.velMin
		if abs(self.angle - ang) < self.rotationSpeed:
			self.angle=ang
		else:
			if(360+ang-self.angle < abs(ang-self.angle)):
				self.angle+=self.rotationSpeed 
			elif(360+self.angle-ang < abs(ang-self.angle)):
				self.angle-=self.rotationSpeed
			elif ang > self.angle:
				self.angle+=self.rotationSpeed
			elif ang < self.angle:
				self.angle-=self.rotationSpeed
			if self.angle >= 360:
				self.angle-=360
			elif self.angle < 0:
				self.angle+=360	
		self.updateVelocity()

	def displayPositionDetails(self):
		w2screen(win,"xpos:"+str(round(self.position.x/xscale)),300,200)
		w2screen(win,"ypos:"+str(round(self.position.y/yscale)),300,250)
		

	def update(self):
		# self.displayPositionDetails()
		self.HitOnMelee()
		self.MindDash()
		self.autoShoot()
		self.HideHealthBar()
		self.ManageInvincibility()
		self.updateRunBullets(win)
		self.updateAndDrawShootPos(win)
		self.updateAndDrawHealthBar(win)
		self.changeWeapons()

		if self.staggering:
			self.staggerBack()
		else:			
			if CPRESSED:
				if self.dashTriggerOn:
					self.dashTriggerOn=False
					if not self.dashOn and time.time()-self.dashStartTime > self.maxDashGap:
						SpawnCloudGroup(self.position)
						whoosh.play()
						self.dashOn=True
						self.dashStartTime=time.time()
			elif not self.dashTriggerOn:
				self.dashTriggerOn=True

			if SPACEPRESSED:
				self.shoot()
			if BPRESSED:
				self.BlockWithGun()
			
			if LEFTPRESSED:
				self.angle-=self.rotationSpeed
				self.IncreaseRotationSpeed()
				if self.angle < 360:
					self.angle+=360
				self.updateVelocity()

			elif RIGHTPRESSED:
				self.angle+=self.rotationSpeed
				self.IncreaseRotationSpeed()
				if self.angle > 360:
					self.angle-=360
				self.updateVelocity()
			else:
				self.rotationSpeed=self.rotationSpeedMin

			if UPPRESSED:	
				if self.runningAnimation()=="idle":
					self.ChangeAnimation("move")		
				self.ApplyVelocity()
			else:
				if self.runningAnimation()=="move":
					self.ChangeAnimation("idle")
				self.DeApplyVelocity()
			

		self.boxCollider.updateP(self.position)

	def updateAndDrawHealthBar(self,win):
		self.healthBar.update(-self.angle,self.position)
		if not self.healthBarHidden:
			self.healthBar.display()
		
	def updateAndDrawShootPos(self,win):
		self.shootPosition.update(self.angle,self.position)
		# self.shootPosition.display()	
	
		
	def updateVelocity(self):
		# rangle=360-self.angle
		self.velocity.x=self.vel * math.cos(d2r(self.angle))
		self.velocity.y=self.vel * math.sin(d2r(self.angle))	


	def ApplyVelocity(self):
		if self.dashOn:
			self.vel=self.vmax=self.dashVelocity
		elif self.vmax!=self.vmaxOrig:
			self.vmax=self.vmaxOrig
			self.vel=0
		if self.vel <= self.vmax:
			self.vel+=1
			self.updateVelocity()
		self.position.add(self.velocity)
		self.checkCollisionWithRoadBlocks()
		

	def DeApplyVelocity(self):
		if self.vel <=self.velMin:
			# self.velocity.set(0,0)
			return True
		self.vel-=1
		self.updateVelocity()
		self.position.add(self.velocity)
		self.checkCollisionWithRoadBlocks()

	def checkCollisionWithRoadBlocks(self):
		for x in gameManager.roadBlocksList:
			if not x.onScreen:
				continue
			if boxCollision(self.boxCollider,x.topCollider):
				self.position.y-=abs(self.velocity.y)
			if boxCollision(self.boxCollider,x.bottomCollider):
				self.position.y+=abs(self.velocity.y)
			if boxCollision(self.boxCollider,x.leftCollider):
				self.position.x-=abs(self.velocity.x)
			if boxCollision(self.boxCollider,x.rightCollider):
				self.position.x+=abs(self.velocity.x)

	def display2(self):
		if not self.FlickerManagerCleared():
			return
		draw_translate_rotate(self.images[self.anim][self.frame],
							  self.angle,self.position.x-self.width/2-gameManager.camera.position.x,
							  self.position.y-self.height/2-gameManager.camera.position.y,win)
		self.updateAnimation()
		#self.boxCollider.display(win)
	def display(self):
		self.rotatedImage=pygame.transform.rotate(self.images[self.anim][self.frame],-self.angle)
		myrect=self.rotatedImage.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y		
		win.blit(self.rotatedImage,myrect)
		self.updateAnimation()		
		# self.updateAndDrawShootPos(win)
###########################Player ends#####################################