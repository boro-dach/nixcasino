import { Body, Controller, HttpCode, Post } from '@nestjs/common';
import { GameService } from './game.service';
import { GameResultDto } from './dto/game.dto';

@Controller('game')
export class GameController {
  constructor(private readonly gameService: GameService) {}

  @HttpCode(200)
  @Post('result')
  async createGameResult(@Body() dto: GameResultDto) {
    const gameResult = await this.gameService.createGameResult(dto);

    return gameResult;
  }
}
