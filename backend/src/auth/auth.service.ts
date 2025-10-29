/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { Injectable } from '@nestjs/common';
import { User } from 'generated/prisma/client';
import { CreateUserDto } from 'src/user/dto/user.dto';
import { UserService } from 'src/user/user.service';

@Injectable()
export class AuthService {
  constructor(private readonly userService: UserService) {}

  async login(dto: CreateUserDto): Promise<User> {
    const oldUser = await this.userService.findById(dto.id);

    if (!oldUser) {
      const user = await this.userService.create(dto);
      return user;
    }

    return oldUser;
  }
}
