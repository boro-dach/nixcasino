/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { Body, Controller, HttpCode, Post } from '@nestjs/common';
import { AuthService } from './auth.service';
import { CreateUserDto } from 'src/user/dto/user.dto';
import { User } from 'generated/prisma/client';

@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @HttpCode(200)
  @Post('login')
  async login(@Body() dto: CreateUserDto): Promise<User> {
    const user = await this.authService.login(dto);

    return user;
  }
}
