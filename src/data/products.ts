export interface ProductLink {
  label: string
  url: string
}

export interface Product {
  slug: string
  name: string
  tag: string
  hue: string
  platform: string
  tech: string
  image: string
  summary: string
  description: string[]
  features: { title: string; text: string }[]
  links: ProductLink[]
}

export const PRODUCTS: Product[] = [
  {
    slug: 'doce-preco',
    image: '/products/doce-preco.png',
    name: 'Doce Preço',
    tag: 'Confeitaria',
    hue: 'var(--rosa)',
    platform: 'iOS',
    tech: 'React Native · TypeScript',
    summary:
      'Precificação e acompanhamento de preços para confeiteiras: calcule custos, compare ofertas e venda com margem certa.',
    description: [
      'Quem vive de confeitaria sabe: o doce pode ser perfeito, mas se o preço estiver errado, o negócio não fecha a conta. O Doce Preço nasceu para tirar a precificação do achismo.',
      'Com ele, a confeiteira registra ingredientes e custos, acompanha variações de preço e descobre quanto cobrar para ter lucro de verdade — tudo pelo celular, sem planilha.',
    ],
    features: [
      { title: 'Cálculo de custo por receita', text: 'Registre ingredientes e quantidades e veja o custo real de cada doce.' },
      { title: 'Margem de lucro clara', text: 'Defina sua margem e receba o preço de venda sugerido na hora.' },
      { title: 'Comparação de ofertas', text: 'Acompanhe preços de produtos e encontre as melhores condições de compra.' },
      { title: 'Feito para o dia a dia', text: 'Interface simples, pensada para quem usa entre uma fornada e outra.' },
    ],
    links: [{ label: 'Baixar na App Store', url: 'https://apps.apple.com/us/app/docepre%C3%A7o/id6761034172' }],
  },
  {
    slug: 'agronet',
    image: '/products/agronet.png',
    name: 'AgroNet',
    tag: 'Agro',
    hue: 'var(--campo)',
    platform: 'Web',
    tech: 'React · TypeScript · Tailwind CSS',
    summary:
      'Gestão agrícola com controle e monitoramento de atividades rurais em uma interface moderna e direta.',
    description: [
      'A rotina no campo gera dados o tempo todo — plantio, insumos, colheita, custos. O AgroNet organiza tudo isso em um sistema web acessível de qualquer dispositivo.',
      'O produtor acompanha as atividades da propriedade, registra operações e enxerga o andamento da produção sem depender de papel ou planilhas espalhadas.',
    ],
    features: [
      { title: 'Controle de atividades rurais', text: 'Registre e acompanhe plantio, manejo e colheita em um só lugar.' },
      { title: 'Monitoramento da produção', text: 'Visualize o andamento das operações da propriedade em tempo real.' },
      { title: 'Acesso de qualquer lugar', text: 'Sistema web responsivo: funciona no escritório, em casa ou no campo.' },
      { title: 'Interface direta', text: 'Sem curva de aprendizado — o essencial na tela, sem enfeite.' },
    ],
    links: [{ label: 'Acessar o AgroNet', url: 'https://agronet.vercel.app/login' }],
  },
  {
    slug: 'cafecontroll',
    image: '/products/cafecontroll.png',
    name: 'CaféControll',
    tag: 'Cafeteria',
    hue: 'var(--cafe)',
    platform: 'Web',
    tech: 'React · TypeScript',
    summary:
      'Controle de produção e vendas de café: estoque, caixa e rotina da cafeteria em um só lugar.',
    description: [
      'Entre o balcão e a máquina de espresso, sobra pouco tempo para gestão. O CaféControll concentra o controle da cafeteria em uma tela só.',
      'Vendas, estoque e caixa registrados no momento em que acontecem — para o dono saber, no fim do dia, exatamente como o negócio está.',
    ],
    features: [
      { title: 'Registro de vendas', text: 'Lance vendas rapidamente, sem travar a fila do balcão.' },
      { title: 'Controle de estoque', text: 'Saiba quando o grão, o leite e os insumos estão acabando antes de faltar.' },
      { title: 'Fechamento de caixa', text: 'Resumo do dia pronto, sem conferência manual.' },
      { title: 'Visão do negócio', text: 'Números do mês na tela para decidir com base em dados.' },
    ],
    links: [],
  },
  {
    slug: 'orgenyx',
    image: '/products/orgenyx.png',
    name: 'Orgenyx',
    tag: 'Produtividade',
    hue: 'var(--lilas)',
    platform: 'iOS & Android',
    tech: 'React Native · TypeScript',
    summary:
      'Organização de tarefas e produtividade diária, com categorização de atividades e acompanhamento de progresso.',
    description: [
      'O Orgenyx é o app de produtividade da Norvia: tarefas organizadas por categoria, progresso visível e uma rotina que finalmente cabe no bolso.',
      'Disponível para iOS e Android, foi desenhado para quem quer constância — planejar o dia, marcar o que foi feito e ver a evolução ao longo das semanas.',
    ],
    features: [
      { title: 'Categorização de atividades', text: 'Separe trabalho, estudos e vida pessoal sem misturar as listas.' },
      { title: 'Acompanhamento de progresso', text: 'Veja quanto do dia (e da semana) você já concluiu.' },
      { title: 'iOS e Android', text: 'O mesmo app, nas duas lojas, com a mesma experiência.' },
      { title: 'Rápido de usar', text: 'Criar uma tarefa leva segundos — o app não atrapalha a rotina.' },
    ],
    links: [
      { label: 'Baixar na App Store', url: 'https://apps.apple.com/br/app/orgenyx/id6760567600' },
      { label: 'Baixar no Google Play', url: 'https://play.google.com/store/apps/details?id=com.orgenyx' },
    ],
  },
  {
    slug: 'organiza-ela',
    image: '/products/organiza-ela.jpeg',
    name: 'Organiza Ela',
    tag: 'Organização pessoal',
    hue: 'var(--rosa)',
    platform: 'iOS',
    tech: 'Flutter',
    summary:
      'Rotinas e tarefas do dia a dia organizadas de um jeito simples, para todos os públicos.',
    description: [
      'O Organiza Ela ajuda a colocar ordem na rotina: tarefas de casa, compromissos e listas do dia a dia em um app leve e acolhedor.',
      'Feito em Flutter para iOS, é pensado para todos os públicos — de quem administra a casa a quem só quer parar de esquecer as coisas.',
    ],
    features: [
      { title: 'Rotinas do dia a dia', text: 'Organize tarefas recorrentes da casa e da vida pessoal.' },
      { title: 'Listas simples', text: 'Crie, marque e conclua sem menus escondidos.' },
      { title: 'Para todos os públicos', text: 'Interface amigável que qualquer pessoa usa sem manual.' },
      { title: 'Leve e rápido', text: 'Abre na hora, funciona no dia a dia corrido.' },
    ],
    links: [{ label: 'Baixar na App Store', url: 'https://apps.apple.com/us/app/organiza-ela/id6772197107' }],
  },
  {
    slug: 'agendamais',
    image: '/products/agendamais.png',
    name: 'AgendaMais',
    tag: 'Agendamento',
    hue: 'var(--ceu)',
    platform: 'Web',
    tech: 'React · TypeScript · Tailwind CSS',
    summary:
      'Agendamento online para gerenciar compromissos e horários com eficiência — do salão ao consultório.',
    description: [
      'Agenda de papel lota, WhatsApp se perde. O AgendaMais é um sistema de agendamento online para prestadores de serviço que querem horários organizados e clientes bem atendidos.',
      'Compromissos, horários e encaixes gerenciados em uma interface moderna — do salão de beleza ao consultório.',
    ],
    features: [
      { title: 'Agenda organizada', text: 'Todos os horários do dia e da semana em uma visão só.' },
      { title: 'Gestão de compromissos', text: 'Marque, remarque e cancele sem retrabalho.' },
      { title: 'Para qualquer serviço', text: 'Salões, clínicas, consultórios e estúdios usam a mesma base.' },
      { title: 'Site de apresentação', text: 'Página de marketing pronta para divulgar o serviço aos clientes.' },
    ],
    links: [
      { label: 'Acessar o sistema', url: 'https://agendamais-x19j.vercel.app/' },
      { label: 'Ver site de apresentação', url: 'https://web-agendamais-6fmq.vercel.app/' },
    ],
  },
  {
    slug: 'lumera-fest',
    image: '/products/lumera-fest.png',
    name: 'Lumera Fest',
    tag: 'Eventos',
    hue: 'var(--sol)',
    platform: 'Web',
    tech: 'React · TypeScript · Tailwind CSS',
    summary:
      'Venda de ingressos para festas e eventos com uma experiência de compra simples e rápida.',
    description: [
      'Vender ingresso não pode ser mais difícil que organizar a festa. O Lumera Fest é uma plataforma de venda de ingressos com experiência de compra direta: escolheu, pagou, recebeu.',
      'Para o organizador, uma vitrine de eventos moderna; para o público, menos cliques entre a vontade de ir e o ingresso na mão.',
    ],
    features: [
      { title: 'Vitrine de eventos', text: 'Cada festa com sua página, arte e informações.' },
      { title: 'Compra simplificada', text: 'Fluxo curto do clique ao ingresso emitido.' },
      { title: 'Interface moderna', text: 'Visual que valoriza o evento e passa confiança na compra.' },
      { title: 'Web e responsivo', text: 'Funciona bem no celular, onde o ingresso é comprado.' },
    ],
    links: [{ label: 'Ver eventos', url: 'https://lumerafest.online/events/' }],
  },
  {
    slug: 'daex',
    image: '/products/daex.png',
    name: 'Daex',
    tag: 'E-commerce',
    hue: 'var(--gold)',
    platform: 'Web',
    tech: 'React · TypeScript · Tailwind CSS',
    summary:
      'Venda de produtos online com catálogo dinâmico e uma experiência de compra moderna.',
    description: [
      'O Daex é a plataforma de vendas online da Norvia: catálogo dinâmico, vitrine organizada e uma jornada de compra pensada para converter.',
      'Produtos bem apresentados, navegação fluida e checkout sem fricção — a base de um e-commerce que vende.',
    ],
    features: [
      { title: 'Catálogo dinâmico', text: 'Produtos organizados e fáceis de encontrar.' },
      { title: 'Experiência de compra moderna', text: 'Navegação fluida do produto ao pedido.' },
      { title: 'Visual profissional', text: 'Vitrine que valoriza os produtos e a marca.' },
      { title: 'Responsivo', text: 'Compra confortável no celular e no computador.' },
    ],
    links: [{ label: 'Acessar o Daex', url: 'https://daex.online' }],
  },
]

export const SOCIALS = [
  { label: 'LinkedIn', url: 'https://www.linkedin.com/in/laysadiniz' },
  { label: 'GitHub', url: 'https://github.com/santosdlaysa' },
  { label: 'Instagram', url: 'https://www.instagram.com/santosdlaysa' },
]

export const CONTACT_EMAIL = 'contato@norviasolutions.com'
