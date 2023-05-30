const { Client, GatewayIntentBits, Partials, EmbedBuilder } = require('discord.js');
// const client = new Client({ intents: ['Guilds', 'GuildMessages', 'MessageContent'] });
const client = new Client({ intents: [GatewayIntentBits.Guilds,GatewayIntentBits.GuildMessages,GatewayIntentBits.MessageContent], partials: [Partials.Channel] });
const prefix='!'
client.on('ready', () => { // ready 이벤트시 실행할 함수
  console.log(`Logged in as ${client.user.tag}!`); // client.user 는 자신의 유저 객체이고 tag 는 유저 객체의 프로퍼티 입니다.
});

client.on('messageCreate', (msg) => { // message 이벤트시 msg (Discord.Message) 매개변수를 받고 실행할 함수
    if (msg.content === '앙') { // Discord.Message 객체의 content 프로퍼티가 'ping' 일 때
        msg.reply('응디'); // reply 는 멘션 + , msg 로 출력됩니다.
    }
});
//투표
//!투표 타이틀 목표1 목표2
client.on('messageCreate', (msg) => { 
    if(msg.content.substring(0,3)==="!투표") {
        const description=msg.content.substring(4)
        temp_str=description.split(" ")
        if( temp_str.length!=3){
            msg.channel.send('형식 !투표 제목 목표1 목표2로 입력해주세요');
            return false
        }
        const exampleEmbed = new EmbedBuilder()
	    .setColor(0x0099FF)
	    .setTitle(temp_str[0])
	    .addFields(
		    { name: '1', value: temp_str[1], inline: true },
		    { name: '2', value: temp_str[2], inline: true },
	    )
	    .setTimestamp()
	    .setFooter({ text: 'made by JYJ'});

    msg.channel.send({ embeds: [exampleEmbed] }).then((msg)=>{
        msg.react("😀")
        msg.react("😥")
        });
    }
});
client.login("MTA2MDEzMjA1MTI3NTIzOTQyNA.Gc2VA6.wEz71EuH9y7TsGKFuMIrNwTpD294Cu5uBeAKhw");
