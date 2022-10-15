<template>
  <div style="height: 100%; background: #002833;">
    <div class="console" id="terminal"></div>
</div>
  
</template>
<script>
    import { Terminal } from 'xterm';
    import { FitAddon } from 'xterm-addon-fit'
    import "xterm/css/xterm.css"
    
  export default {
    name: 'webssh',
    data () {
      return {
        
        term: '',
        terminalSocket: null,
        order:''
      }
    },
    methods: {      
    },
    mounted () {
      let data = this.$route.query
      console.log(data)
      
      var term = new Terminal({
        cursorBlink: true,
        rows: 40,
        cols: 130
      });

      term.open(document.getElementById('terminal'));

      var socket = new WebSocket(
        'ws://127.0.0.1:8000/webSsh/?namespace='+ data.namespace + '&name=' + data.podName);

        term.onKey(e => {
            const ev = e.domEvent
            const printable = !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey
            if (ev.keyCode === 8) {
                // Do not delete the prompt
                if (term._core.buffer.x > 2) {
                    term.write('\b \b')
                }} else if (printable) {
                term.write(e);
            }
            socket.send(e.key);
            
        });

        socket.onerror = function (event) {
          console.log('error:' + e);
        };

        socket.onmessage = function (event) {
          term.write(event.data);
        };

        socket.onclose = function (event) {
          term.write('\n\r\x1B[1;3;31msocket is already closed.\x1B[0m');
          // term.destroy();
        };
      // };
    }
     
  }
</script>