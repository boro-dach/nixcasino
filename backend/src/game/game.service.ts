import { Injectable } from '@nestjs/common';
import { PrismaService } from 'src/prisma.service';
import { GameResultDto } from './dto/game.dto';
import { UserService } from 'src/user/user.service';

@Injectable()
export class GameService {
  constructor(private readonly prisma: PrismaService) {}

  async createGameResult(dto: GameResultDto) {
    const gameResult = await this.prisma.gameResult.create({
      data: dto,
    });

    await this.prisma.user.update({
      where: { id: dto.userId },
      data: {
        gamesPlayed: { increment: 1 },
        turnover: { increment: dto.profit },
        balance: { increment: dto.profit },
      },
    });

    return gameResult;
  }
}
